# Task 30: three closer global examples, gap 5's portal check, one report rebuild (hq, Fable, 2026-10-30)

Repo: `D:\Projects\engineering\onyx-hackathon-build`. Base: `main` at tag `task-29` (name the commit). Branch `task-30`.
Words and data only: no gate, key, scenario, run, prompt or eval change. USD 0. Opus, about 3 hours, by 2026-11-02.
Ruling: `perplexity-2026-10-30/sweep-4b-read-2026-10-30-fable.md` section 4 (the quotes, verified at the primary).

## A. Three KB source files, VERIFIED

Fetch each from the issuing body, store the text under `kb/sources/global/`, add a manifest row with URL, sha256,
language, status VERIFIED, binding_status as below, and `kb verify` passing. Follow the existing global rows' column
conventions exactly (open `canada-ola-part-iv` and `eu-crd-2011-83-art8` first).

| id | source | URL | lang | binding |
|---|---|---|---|---|
| `es-ley-10-2025` | Spain, Ley 10/2025 de 26 de diciembre, servicios de atención a la clientela, BOE-A-2025-26698 | `https://www.boe.es/boe/dias/2025/12/27/pdfs/BOE-A-2025-26698.pdf` (PDF; text by pdftotext; join each paragraph to one line so quotes match; keep the whole law) | es | binding |
| `wales-wls-no1-2015-sch1` | Welsh Language Standards (No. 1) Regulations 2015, SI 2015/996 (W. 68), Schedule 1 | `https://www.legislation.gov.uk/wsi/2015/996/schedule/1/made/data.xht?view=snippet&wrap=true` (the site answers 202 to some clients; curl with a browser User-Agent works) | en | binding |
| `us-tsr-16cfr310` | US Telemarketing Sales Rule, 16 CFR Part 310, §310.3 | `https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310` (official; the Cornell mirror is not the source) | en | binding |

If the existing quote check is whitespace-sensitive, make the source files match it (one paragraph per line); do not
change the checker. If a fetch fails after two routes, stop and ask with the HTTP status.

## B. Register rows (`onyx/data/gaps.json`), then regenerate `docs/gaps.md`, README register, site

Add to `global_examples`, each with document, clause, file, status VERIFIED and the verbatim quote from the stored
text (Spanish verbatim; no translation in the quote field). Existing examples stay.

- **gap-1:** Ley 10/2025 Art 8(2), two quotes: the "en cualquier momento de la interacción, desde su inicio" sentence
  and the "95% ... en un plazo inferior a tres minutos" sentence; Art 8(3), the "en el transcurso de esa misma
  comunicación" sentence. Add to `recommendation` one clause: the TDRA time can take Spain's shape (a human on request
  at any moment; 95% of requests within three minutes). Add to `uae_position` or the row's note the scope line:
  Art 2(1)(d) covers electronic communications; Art 2(6) sector rules first, this law supplementary.
- **gap-10:** Wales Sch 1 Standards 15, 22 and 60, verbatim. Note the scope: public bodies under a compliance notice
  (reg 2(1)(b)), not operators.
- **gap-11:** 16 CFR 310.3(a)(3)(ii), the lead sentence through "receipt of all of the following information:" and
  items (A) to (H) as one quote.
- **gap-5:** add to `uae_position`: "Checked 2026-10-30 on uaelegislation.gov.ae: the related-legislations page of
  Decree-Law 45/2021 lists only Decree-Law 30/2024 and Decree-Law 26/2025; no executive regulation and no Cabinet
  resolution. A vendor blog's 'Cabinet Decision No. 111/2023' has no instrument on the portal." In `kb/manifest.csv`,
  row `pdpl-executive-regulations`, notes: "Not issued as of 2026-10-30 (portal related-legislations checked)".

## C. Report (`docs/report.md`, rebuild `docs/report.docx` once)

Global-example cells only, same length or shorter:
- Row 1: `IMDA 2.2.2, 2.4.2` becomes `Spain Ley 10/2025 Art 8(2), 8(3)`
- Row 10: `Canada OLA ss. 22, 26, 27` becomes `Wales WLS Regs 2015 Sch 1 Std 15, 22`
- Row 11: `E-Commerce Dir. 2000/31 Art 11(2)` becomes `US TSR 16 CFR 310.3(a)(3)(ii)`

Introduction counts: "51 documents", "47 are verified", "nine foreign texts" become the values `kb verify` prints
after Part A (expected 54, 50, twelve); read, never typed; `build_report.py` checks them if it does not already.
README and `kb/DATASHEET.md` counts regenerate the same way.

Page count with `scripts/report_pages.ps1`. If Word says 6, cut in this order, one at a time, recount after each:
(1) gap 9 row: delete `, and Resolution 106/2026's age checks reach social media only (Art 2)`; (2) gap 2 row:
delete `, so a spoken "yes" buys the service`; (3) stop and ask with page and word count.

## Checks (show each output)

- [ ] `python -m onyx kb verify`: three new VERIFIED rows; counts printed.
- [ ] Quote test: every new `global_examples` quote found verbatim in its file.
- [ ] `check-data`, `python -m onyx gaps`, `python -m onyx site`: byte-identical on a second run.
- [ ] `test_report_figures_match_eval` and the Part D tests still pass; full suite passes (552 + new).
- [ ] `git diff <base> -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/ onyx/model.py onyx/prompts` prints nothing.
- [ ] `pages: 5` pasted.
- [ ] hq copy: `docs/report.md` over `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md`, previous kept as `.bak-2026-11-0x`.
- [ ] Commit `kb, gaps, report: Spain 10/2025, Wales WLS 2015, US TSR as global examples; gap 5 portal check`; PR; CI green; report-back in `docs/report-back/` with the Limits line (seven layers, each shipped or deferred; no prompt change, so no prompt evals due) and the count check.

**Stop and ask when:** a quote cannot be matched verbatim after the paragraph join; `kb verify` counts differ from
54 / 50 / 12; page 6 survives cut 2; anything outside the files named here needs to change.

## Not in this order

Any change to gates, keys, scenarios, runs or prompts; the video; the submission-day list; another team or another team text
anywhere in the repo (competitor names stay out).
