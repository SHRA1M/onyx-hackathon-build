# Report-back: Task 35b, bot-disclosure statutes into the KB and register (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-35b-bot-disclosure.md` (hq's order file as of 2026-10-30, with the four URLs
and the HSC date hq added; Addendum B is the build). Base `main` 9fb5e1f (PR #11 merged on Iyas's word), branch
`task-35b`, PR #12. Opus 5.5, one session. USD 0: no model call.

**Limits:** KB manifest rows, local-sources, datasheet, export, intent, the register (`onyx/data/gaps.json`, its
renderers in `onyx/gaps.py` and `onyx/site.py`, `data.cited_chunks`), `docs/gaps.md`, the site, the README's two count
lines and register table, the report's gap 6 cell and three count lines, tests, CHANGELOG. Fetched only the URLs
Addendum B names. No chunks, no runs, no gate, rule, mandate, prompt, eval, model or agent file (`git diff --stat main
-- runs onyx/gate.py onyx/agents eval kb/chunks onyx/data/rules.json onyx/data/mandates.json onyx/data/keys
onyx/data/scenarios onyx/model.py`: empty). Seven layers unchanged. Owner of any failure: Iyas.

## Summary

Gap 6 now leads with a binding statute already in force in general commerce (Maine), not an EU Regulation that applies
from 2026-08-02. Gaps 1 and 7 gain the one telecom-regulator text we hold that orders an automated channel to offer a
person (India TRAI reg 3(9)). Five KB rows: 88 documents, 83 VERIFIED, 34 foreign. The report changes in one cell
(gap 6) and its three count lines, and stays at 5 pages.

## What differs from the order, and why

1. **California rows are VERIFIED with kind `extract`, not REFERENCED.** The schema has the extract kind (same choice
   as Addendum A's Qatar row). The extract files sit in `kb/sources/global/` (local only, gitignored, the eIDAS and
   COPPA pattern) and carry only the read file's quotes, copied by script from its table. `http_status` is 403, as
   curl gets; the notes say that hq loaded both pages in a browser (200).
2. **Texas: the stored page holds no statute text.** `texas-bcc-552.html` hashes equal to a fresh fetch, but it is the
   site's script app; the chapter loads by script. The row is VERIFIED as ordered, and its note says this. The
   §552.051(b), (c) quotes are checked against hq's read file, not the stored bytes. "eff. January 1, 2026" comes from
   the order and the read file, not from bytes I could read.
3. **India quotes are taken from the PDF text layer, not the read file's table.** The table elides (b) with "..." and
   prints "manner:" where the PDF has "manner:-". Two verbatim pieces: the opening of reg 3(9) (PDF page 4) and the
   proviso (page 5). Nothing was typed.
4. **California §17941 is two example entries, (a) and (b).** The register holds one quote per entry.
5. **Korea and the TRAI draft have no KB row**, so a `searched` entry may now name a `url` instead of a stored file
   (renderer in `gaps.py` and `site.py`; `cited_chunks` and two register tests skip it as they skip `file`). Korea's
   quote is checked against hq's stored KLRI page: its URL bytes differ from that file (as the order expected: the
   article loads by script). The TRAI draft was fetched from its named URL (200, sha256 `3acbc938...35116`, 76 pages).
   Its quote "new-age customer-centric solutions (Chatbots, AI Agents, etc.)" is on PDF page 10, proposed reg 3(11),
   and the draft also substitutes reg 3(9). That check ran in the build; no test repeats it, because the draft is not
   stored.
6. **Preamble sentence:** "The 2025 to 2026 US statutes on chatbots regulate companions and carve out customer
   service." It appears in `docs/gaps.md` and the site, but not in the README paragraph, which Addendum B does not name.
7. **Existing pins extended, not loosened:** the KB count pins (two in `test_kb.py`), `test_report.py`'s count strings,
   the README count lines, gap 7's "Utah, Moffatt, Moffatt" (now the first three), Task 35's tail slices (they skip
   the 35b entries that follow), and Task 32's "file entries come last" (URL entries count with them).

## Decisions taken in the build

- Document ids: `maine-1500-dd`, `india-trai-tccrr-2012`, `texas-bcc-552`, `california-bpc-17940-17943`,
  `california-hsc-1339-75` (hq's file names, lowercase; "california" because "ca-" already means Canada here).
- Gap 6's replay-page example is now Maine §1500-DD(2): the first binding example, with no marker needed. This matches
  the report cell. No recorded run flags gap 6, so no replay page changed.
- India reg 3(9) carries a different `says` on gap 1 (the order's gloss) and gap 7 (conduct rule, nothing on AI
  identity, no clock).
- `PR #11` was merged on Iyas's word; `task-35` was **not tagged** (not asked). The brief's habit is to tag after a
  merge: say the word and I will.

## Done means

Fresh fetch of each row URL against the filed copy:

```
 200  fresh 85e41c95d590  filed 85e41c95d590  manifest 85e41c95d590  downloaded, equal          maine-1500-dd
 200  fresh 5d0b0da12fc5  filed 5d0b0da12fc5  manifest 5d0b0da12fc5  downloaded, equal          india-trai-tccrr-2012
 200  fresh dbfba8a96dc3  filed dbfba8a96dc3  manifest dbfba8a96dc3  downloaded, equal          texas-bcc-552
 403  fresh -             filed cfa4c3ccba6c  manifest cfa4c3ccba6c  local copy (extract file)  california-bpc-17940-17943
 403  fresh -             filed 86d9eda28fb0  manifest 86d9eda28fb0  local copy (extract file)  california-hsc-1339-75
```

No mismatch, so no stop. `kb verify` (up by 5 VERIFIED; foreign 29 to 34 in the datasheet):

```
VERIFIED 83  REFERENCED 2  UNVERIFIED 3  HISTORICAL 0
  every fetched source matches its sha256
```

Datasheet: `88 manifest rows, one per document, 67 instruments`; `| foreign | 34 |`.
`check-data ok: every quote verbatim, every rule cites a clause`.

Report tries, in the order's sequence (`docs/build_report.py`, then `scripts/report_pages.ps1`):

```
base (counts only)                                   pages: 5  words: 2192
gap 1 "; Saudi CST 552/1445 §13.1, 26.5.2"           pages: 6  words: 2197   left out
gap 6 "Maine §1500-DD; EU AI Act Art 50(1)"          pages: 5  words: 2193   kept
gap 7 row (Utah; India reg 3(9))                     pages: 6  words: 2221   left out
gap 3 "; Qatar CCPR 2024 §1.2"                       pages: 6  words: 2197   left out
final                                                pages: 5  words: 2193
```

Each time it overflowed, page 6 began with "Before the final: the seven unseen scenarios run cold, ...". hq's
`report-draft-2026-10-23.md` was **not** updated: this build writes nothing outside the repo. hq copies
`docs/report.md` if it wants the copy kept equal.

Served site (`docs/site/gaps.html` over http on 127.0.0.1, Playwright):

```
companion true, gap6_order Maine 1 < California 733 < EU AI Act 1652, texas true, korea_link true,
trai_draft_link true, draft_label true, india_in_gap1 true, india_in_gap7 true, hsc_in_gap7 true,
hsc_searched_gap1 true, arabicQuotes 57, allRtl true, brazil false
```

The only console error was `favicon.ico` 404 from the local server.

Full suite: `630 passed` (621 before; nine new). New tests: `test_task_35b_five_rows_are_verified_foreign_binding_
with_no_chunks`, `..._row_notes_print_only_what_the_page_prints`, `..._california_extracts_carry_exactly_the_read_
files_quotes`, `..._counts`, `..._gap_6_maine_leads_california_second_the_ai_act_third` (and the report cell, the
replay example), `..._gap_7_and_gap_1_examples_are_appended`, `..._searched_entries_are_appended_last`, `..._quotes_
are_verbatim_in_the_stored_text` (13 quotes), `..._entries_render_on_the_register_and_the_site`.

All of CI's generators were rerun locally (kb verify, check-data, datasheet, intent, gaps, replay-page, model-down,
replay-page --html, eval twice, report build, figures, site); no file changed after them. CI on PR #12
(https://github.com/SHRA1M/onyx-hackathon-build/pull/12): `reproduce pass` (runs 41143492917 and 41143513192, push
and pull request). Not merged, not tagged.

## Merge danger and blast radius

A two-way door: data rows, register entries, one renderer branch and count lines, all regenerated from the manifest and
`gaps.json`. No run, gate or key moves; replay verdicts are untouched. Reverting the branch restores Task 35 exactly.

## Open questions for hq

1. The two California extracts and the Maine and India derived texts exist only in this repo's gitignored
   `kb/sources/global/`. If they are lost, the California hashes cannot be re-made byte for byte. hq may want copies
   under `standards-text/bot-disclosure-2026-10-30/` (I write nothing outside the repo).
2. Texas is VERIFIED on a hash of a page that does not hold the text. Should the row stay VERIFIED, or become an
   extract like California?
3. The report still has no gap 7 row and no Gulf text in gaps 1 and 3. Any of them needs a cut elsewhere: 1 to 28
   words push the report to page 6.
4. In-force dates not verified: Maine (session general effective date only), India TCCRR's Gazette date, Korea Art 31.
