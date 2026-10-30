# Report-back: Task 30, three closer global examples, gap 5's portal check, one report rebuild (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-30-global-examples.md` (hq, Fable, 2026-10-30). Ruling:
`perplexity-2026-10-30/sweep-4b-read-2026-10-30-fable.md` section 4. Base: `main` at e4c3b75 (the wrap commit after
tag `task-29`, which points to bf44cce). Branch `task-30`. Opus 5.5. USD 0.

**Limits:** words and data only. Changed: three KB source files (local, gitignored), `kb/manifest.csv`,
`kb/local-sources.json`, `kb/manifest.schema.json` (one pattern, Iyas's go), `onyx/data/gaps.json`, `onyx/gaps.py`
(three short labels), `docs/build_report.py` (the count check), `docs/report.md`, `docs/report.docx`, `README.md`,
tests, and the regenerated `docs/gaps.md`, `docs/site/`, `docs/intent.json`, `kb/DATASHEET.md`,
`kb/export/InputDocs/Inputs.md`. On failure it stops and asks: no model call, nothing recorded, nothing sent
outward, nothing under `runs/` or `onyx/data/keys/`, no gate, rule, mandate, eval, model or prompt file changed (check
5 below). Owner of any failure: Iyas.

**The seven layers** (`hq/_reference/llm-agents.md`). Task 30 changes no prompt, so no prompt evals are due.
1. Versioned prompt: shipped (v5 on every C5 run_start); unchanged.
2. Grounding: shipped (clause ids and verbatim quotes, `check-data` ok); unchanged.
3. Tools under a gate: shipped (`gate.py`); unchanged.
4. Asker's identity on tool calls: deferred. A CLI over a synthetic operator with no user accounts.
5. Injection and masking: injection shipped (`run --inject`); outbound PII mask deferred, the subscribers are synthetic.
6. Cost cap: shipped (`cost.TOTAL_CAP_USD`, `--max-usd`); recorded spend still USD 21.85; cache and router deferred.
7. Trace and evals: shipped (hash-chained logs, `verify-log`, `replay`, the full suite); every check rerun below.

## Summary

Spain's Ley 10/2025, the Welsh Language Standards Schedule 1 and 16 CFR 310.3 are in the KB as VERIFIED, quoted in
the register for gaps 1, 10 and 11, and lead the report's global-example cells for those rows. Gap 5 records the
portal check. The report's KB counts are now checked against the manifest by the build. Still 5 pages.

## What differs from the order, and why

1. **Schema.** `kb/manifest.schema.json` allowed language `en` or `ar` only, and a test enforces it. Stopped and asked;
   Iyas allowed widening the pattern to `es` (2026-10-30). One line.
2. **eCFR route.** The ecfr.gov page answers 302 to `unblock.federalregister.gov` (an access check) for curl. Second
   route, same official host: the eCFR versioner API, as the existing `us-47cfr-64-2010` row does. Source line:
   `https://www.ecfr.gov/api/versioner/v1/full/2026-10-28/title-16.xml?part=310&section=310.3`; manifest `url` is the
   order's page URL, the API named in `notes`. Stored text is section 310.3 only, footnote marks in brackets.
3. **Spain text.** pdftotext already gave one paragraph per line; page headers and footers dropped, and a line that
   ends mid-sentence joined to the next (the title, page breaks). The 95% sentence holds a narrow no-break space
   (U+202F) between "95" and "%"; the quote keeps it, verbatim.
4. **Scope lines in `note`.** Gap 1's Art 2(1)(d) / Art 2(6) line and gap 10's reg 2(1)(b) line went into each row's
   `note` (shown under the heading on `docs/gaps.md` and the site), because a test pins gap 1's `uae_position` ending.
   `tests/test_site.py` listed gap-12 as the only noted row; it now lists gap-1, gap-10, gap-12.
5. **Code outside the named files.** `onyx/gaps.py` needed short labels for the three new files (`Spain Ley 10/2025`,
   `Wales WLS`, `US TSR 16 CFR`) or `gaps` would crash. Two existing tests read "47 VERIFIED" and "51 rows" literally;
   they now read the counts from the manifest.
6. **hq backup name.** `report-draft-2026-10-23.md.bak-2026-10-30` already existed (a different earlier version), so
   the previous draft is kept as `.bak-2026-10-30-task-30`; nothing overwritten.
7. **No cuts.** Word said 5 pages on the first count, so neither gap 9 nor gap 2 was cut.

## Count check

`kb verify` after Part A, and the manifest:

```
VERIFIED 50  REFERENCED 1  UNVERIFIED 3  HISTORICAL 0
  every fetched source matches its sha256
rows 54, VERIFIED 50, foreign 12
```

| Report / README text | Source |
|---|---|
| "holds 54 documents", "**SRC-2** 54 documents" | 54 manifest rows (`check_kb_counts`) |
| "50 are verified" | VERIFIED 50 |
| "twelve foreign texts" | 12 rows `jurisdiction` foreign |
| README "50 VERIFIED ... 1 REFERENCED ... 3 UNVERIFIED", "(54 rows" | same counts; `test_readme_kb_counts_are_the_manifests` |
| DATASHEET and site cards | regenerated from the manifest |

`build_report.py` now fails on any of the three phrases when it differs from the manifest
(`test_report_build_refuses_a_wrong_kb_count`).

## Checks

1. `kb verify`: three new VERIFIED rows (`es-ley-10-2025`, `wales-wls-no1-2015-sch1`, `us-tsr-16cfr310`); counts above.
2. Quote test: `test_task_30_quotes_are_verbatim_in_their_files` finds all 7 new quotes; the generic verbatim test passes.
3. `check-data` ok; `gaps`, `site`: hash of every changed doc identical on a second run (`367869f1...` twice).
4. `test_report_figures_match_eval` and the Part D tests pass; full suite **568 passed** (552 + 16 new).
5. `git diff refs/tags/task-29 -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json onyx/eval.py runs/ onyx/model.py onyx/prompts`: empty.
6. `scripts/report_pages.ps1`: `pages: 5`, `words: 2215`.
7. hq copy: `docs/report.md` sha256 c7aa325d... equals `hq/uni/ai-for-good-hackathon/report-draft-2026-10-23.md`.
8. Commit 507d721 on `task-30`, PR #5, CI run 41058857982 `completed success`: "556 passed, 12 skipped" (the 12
   read the gitignored `kb/sources/`, which CI does not hold). Merge and tag wait for Iyas.

## Open questions for hq

1. The Wales scope line (reg 2(1)(b)) is not in the stored file, which holds Schedule 1 only; it rests on the ruling's
   read. Store the regulations' body too, or leave it?
2. Gap 10's `recommendation` still names Canada OLA ss. 26 and 27; the report cell now names Wales. Fine as is?

## Task 30b: Wales scope citation (order 2026-10-30-task-30b-wales-scope-fix)

Built on `task-30`, same PR #5. Answers open question 1 above; question 2 is settled by hq (gap 10 keeps naming
Canada, both examples held).

- Fetched regulation 3 as made: `https://www.legislation.gov.uk/wsi/2015/996/regulation/3/made/data.xht?view=snippet&wrap=true`
  (curl, browser User-Agent, HTTP 200). Reg 3(1) reads word for word as the order quotes it.
- Stored text `wales-wls-no1-2015-sch1.txt`: reg 3(1) and 3(2) inserted above Schedule 1, marked "Regulation 3, as made
  (added 2026-10-30, Task 30b)". Both local copies (`kb/sources/` and `kb/sources/global/`) changed alike. sha256
  `7fd3f8f4...` (43,169 bytes) to `6e6c99d1...` (43,943 bytes); manifest row updated (hash, size, notes).
- `reg 2(1)(b)` to `reg 3(1)` in gap-10's note, `docs/gaps.md`, `tests/test_gaps.py`, and the manifest row's notes (the
  same wrong citation sat there; the order did not list it). `docs/site/gaps.html`, `docs/site/kb.html` and
  `kb/export/InputDocs/Inputs.md` regenerated from them.
- `test_task_30_quotes_are_verbatim_in_their_files` also checks the reg 3(1) sentence: failed on the old stored text,
  passes on the new.

Checks: `kb verify` VERIFIED 50, REFERENCED 1, UNVERIFIED 3, every fetched source matches its sha256 (54 documents, 12
foreign, unchanged). `check-data` ok. `grep -rn "2(1)(b)" onyx/ docs/gaps.md tests/`: nothing. Full suite 568 passed.
`scripts/report_pages.ps1`: pages 5, words 2215 (no report text change; the report never cited reg 2(1)(b)).

Differs from the order: the manifest `url` still names Schedule 1; reg 3's address is in the row's notes and the
stored file's header. No change to gates, keys, runs, prompts or eval. USD 0 model spend.
