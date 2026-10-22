# Order: Task 16, pages on citations, one grounding line per scenario, README in our own words, candidate-79bis-2 wording (hq, Fable, 2026-10-22)

Build model: Opus 5.5. No model calls; USD 0. Starts after Task 15 (7313ead, wrap bac8378). Copy this file into
`docs/work-orders/` first. Recorded runs replay as recorded; nothing here changes keys, `rules.json` gate logic, or
any committed chunk line.

Why (hq competitor read 2026-10-22, `docs/sources/competitor-read-2026-10-22.md` once copied): of nine public UAE
entries, three run. Where they are ahead of us: another team shows the page of every citation, another team grounds each
scenario in a real incident and has its report in the repo. Where nobody matches us: a consumer on the line, gates
written from binding UAE clauses, Arabic parity. Our README follows another team's skeleton (ideas, not code). This
order closes the first two and makes the README say what is ours, with no new model run.

## Sources allowed, and nothing else

The committed `kb/chunks/` (every cited chunk carries `page`), `kb/manifest.csv` (`url`, `page_count`, the landing
page mark), `onyx/data/rules.json` (`document_id`, `chunk`), the PDFs under `kb/sources/` for the page test, and four
files hq copied to `docs/sources/` on 2026-10-22: `opening-figure-read-2026-10-20.md` (URLs and quotes for the e&,
TDRA and Etisalat sources), `eand-sustainability-report-appendices-2025.txt`, `tdra-sustainability-report-2023-en.txt`,
`tdra-sustainability-report-2023-ar-p33-36.txt`, plus `competitor-read-2026-10-22.md`. Arabic for 79 bis: the
2026-10-17 law file already in `docs/sources/`, rows "79 bis (1)" and "79 bis (2)". No fetch in this task.

## Facts hq checked (2026-10-22)

- Every chunk in `kb/chunks-full/` and `kb/chunks/` has a `page`. The 16 UAE texts carry real spreads (CPR 70
  distinct pages of 74; licence 43; Telecom Law 32). Four documents carry `page: 1` on every chunk because their
  text had no page markers: `itu-t-y3172` (34-page PDF), `imda-mgf-agentic-v1-5`, `eu-ai-act-2026-07-27`,
  `gdpr-art22`. That 1 is a placeholder, not a page.
- `docs/gaps.md` already prints "(page N)" on every searched row. The replay pages, the replay viewer and the KB
  export do not.
- Seven CPR chunks, one QoS and two Spam Calls chunks carry a stray running footer ("Page 58") inside `text_en`
  (committed, quoted by keys). Leave them; note only.
- Task 15 report item 5: local `kb/chunks-full/` is older than the committed `kb/chunks/`. Page lookups read
  `kb/chunks/` only. A cited id missing there prints no page; do not add chunks for it.

## Items

1. **Pages on citations.** One helper, `page_of(document_id, clause)`, reads `kb/chunks/`. Returns the page when
   the document's committed chunks carry more than one distinct page value, else `None` (the four placeholder
   documents print no page; no re-chunking). Then:
   - `replay_page.py`: a proposal's cite prints `tdra-cpr-v2-en:26.7.2 (p. 65)`; a gate rule line prints
     `CPR 26.7.2, p. 65: "..."` using the rule's `document_id` and `chunk`.
   - `replay_viewer.py`: the same two places. Where the manifest row's `url` is the document itself (not marked
     landing page) and is a PDF, the page is a link to `url#page=N`; a landing-page row gets text only.
   - `kb export`: the per-document table adds a `Pages` column from `page_count` (blank where blank).
   - Label the number "p." everywhere: it is the PDF page index, which can differ from the number printed on the
     page.
   Page test, three clauses, by opening the PDF in `kb/sources/` with pypdf at the chunk's page and finding the
   first 40 characters of the committed quote on that page: CPR 26.7.2 (p. 65), licence 16.3.2 (p. 45),
   Telecom Law 79 bis (p. 29). A miss on any of the three: stop and ask; do not shift pages by hand.
2. **One grounding line per scenario**, English, in each scenario JSON as `grounded_in` (`clause_id`, `page`,
   `line`), printed by `replay-page` under the title as "Grounded in: ..." and shown in the README scenarios table
   as a new last column `grounded in` (clause id and page only). The lines, verbatim; each chunk was read by hq:
   - S1 `tdra-cpr-v2-en:17.4.1` (p. 51) (ruling 2026-10-22, option c, replaces the 17.4 line): "CPR 17.4 and
     17.4.1 require the operator, where possible and practicable, to provide a facility that tells a roaming
     subscriber the applicable retail roaming prices for calls and SMS; the price question in step 2 is the one
     that facility answers."
   - S2 `tdra-cpr-v2-en:4.20.1` (p. 17): "CPR 4.20.1 requires a PIN or TDRA-approved 2FA for each and every content
     purchase, premium channels included; the AED 45 charge with no consent record is the charge that rule exists
     to stop."
   - S3 `pdpl-45-2021-en:23(1)` (p. 25): "PDPL 23(1) lets personal data leave the State only in listed cases, one
     being a contract binding the foreign recipient to this law's controls; the model provider abroad is such a
     recipient."
   - S4 `tdra-cpr-v2-en:22.1.1` (p. 58): "CPR 22.1.1 requires, wherever possible, an individual notice and warning
     before a disconnection for non-payment; step 1 fires with `warning_sent: false`."
   - S5 `decision-16-2026-ar:4.18` (p. 10) and `tdra-cpr-v2-en:26.11` (p. 66): "Decision 16/2026 4.17 and 4.18 make
     the operator verify the reporter's identity at once and block a lost device within two hours; CPR 26.11 lets
     TDRA order a service restored while a dispute is open."
   If a chunk does not say what its line says, stop and ask.
3. **README reframed.** Exact text; everything not named here stays.
   - First paragraph, replaced in full: "Mizan puts a consumer on the line. It is a consumer-care AI for a
     synthetic UAE operator, Team Onyx's entry to the ITU AI for Good Lab Hackathon UAE 2026 (telecom track):
     agents propose each step of a chat or call, plain-code gates written from binding UAE clauses allow or block
     it, and the same gates run in Arabic and English from the same clauses. Every step is written to a
     hash-chained log that replays offline, with the clause, its page and its words."
   - New second paragraph, heading `## Why`: "e& reported 371,476 customer complaints in its UAE operations for
     2025 (e&, Sustainability Report Appendices 2025, Appendix 1, PDF page 7). TDRA dealt with 23,464 complaints
     about licensees in 2023, the latest count it has published (TDRA, Sustainability Report 2023, p. 34). At the
     operator the first contact is already an AI: Etisalat's Virtual Assistant, "AI (Artificial Intelligence)
     powered", 24/7, English or Arabic, whose listed jobs include "adding or deleting services, changing of
     packages" and "Billing related clarifications". No source on file says what stops such an AI when a chat
     becomes a complaint or a disconnection. The binding texts do, and Mizan's gates are written from them." Each
     of the three sources is a link, URL taken from `docs/sources/opening-figure-read-2026-10-20.md`; the two
     figures and the three quoted phrases are tested verbatim against the copied text files and that read.
   - New third section, heading `## Three things to look at first`, three bullets: (1) a consumer on the line:
     five scenarios of a subscriber in a chat or call, not an institution in a drill; (2) gates from binding UAE
     clauses: every allow and block names the clause, its page and its words, in `docs/replay/`; (3) Arabic parity:
     the same gates and keys in both languages, action recall 0.96 English / 0.94 Arabic on C5 (`eval/results.md`).
   - Heading "Two-minute check" becomes "Run it without a key"; "Limits" becomes "What we do not claim"; the
     last bullet there becomes: "No source on file shows how a UAE operator's assistant is governed; the Etisalat
     Virtual Assistant page lists what it does, not what stops it."
   - Nothing added about other entries. No competitor is named anywhere in the repo.
4. **Candidate-79bis-2 row, rewritten** (hq's review of the Task 15 wording; the builder-chosen category, `line`
   labels and `competitor: not read` stand):
   - `gap`: "The Cabinet schedule of licensee violations and fines that Telecom Law 79 bis (2) promises (fines up to
     AED 10,000,000 a violation) is not published; the only published telecom fine schedule, Cabinet 57/2024,
     covers the Telemarketing Regulations. Until it exists, a CPR breach by an automated channel sits in the
     79 bis (1) and licence 16.3.2 band, AED 50,000 to 200,000, doubled under licence 16.3.3 for repetition, a
     missed date or a material failure."
   - Searched rows add `licence-2-2026:16.3.3` (p. 45) with its chunk line, and Arabic for 79 bis (1) and (2) from
     the law file rows (the law file line 43: Arabic prevails).
   - UAE position: "Searched 2026-10-16 on the legislation portal and the web, both languages: not found. Whether
     the Board may fine a licensee under 79 bis (2) before the schedule exists is not stated in the text (inferred
     gap, hq 2026-10-22)."
   - Recommendation unchanged. Report line and README register regenerate from `gaps.json`.
5. **Tests fail first then pass**: `page_of` returns 65 for CPR 26.7.2, 22 for licence 9.1, `None` for any
   `itu-t-y3172` id; the three-clause PDF page test; all five `grounded_in` ids resolve to committed chunks; the
   two README figures and three quoted phrases verbatim in the copied sources; README register row text equals
   item 4; `gaps` and `replay-page` byte-identical on a second run. Full suite, CI green, commit, push. Report
   under 15 lines to `docs/report-back/2026-10-2X-task-16-pages-grounding-readme.md`, naming any wording the build
   changed and why.

## Rulings on the build's first stop (hq, 2026-10-22)

1. **Go.** Add to `kb/chunks/` the lines for CPR 17.4, 17.4.1 and 4.20.1 and licence 16.3.3, copied from the local
   `kb/chunks-full/` as Task 15 did. No existing line changes. Before adding, diff each against the committed
   format (spacing fixes, Task 15 report item 5) and apply the same fixes if they apply.
2. **Option c.** The S1 line is reworded above and now cites 17.4.1. Neither clause says "before the line is used
   abroad", so that phrase is gone.
3. **PDF test with spaces removed** is accepted.

## Stop and ask when

- A page test misses, or a `grounded_in` chunk does not say what its line says.
- A README figure or quoted phrase is not verbatim in the copied source file.
- Anything needs a model call, a fetch, a key change, or a committed chunk line changed.
- A source URL for the `## Why` paragraph is missing from the opening-figure read.

## Rulings on the report-back (hq, 2026-10-22, after Task 17)

All accepted as built; nothing to build. File these rulings into `docs/work-orders/` beside this order and clear them
from the build's background and brief.
1. `page_of` returns None only when every committed chunk of a document says page 1 (report-back item 2). Accepted:
   it keeps the intent (hide Y.3172's placeholder page) without hiding real pages of four other documents.
2. S1 `grounded_in` lists 17.4 and 17.4.1 (item 3). Accepted: the committed-chunk test requires 17.4 to be cited.
3. The competitor read lives in hq only (item 7). Already settled; stays.
4. The two entry names in this filed order: not now. hq strips them before 2026-11-09 with the clean-history public
   repo; the name test keeps skipping `docs/work-orders/` until then.
