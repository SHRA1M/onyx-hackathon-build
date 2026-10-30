# Report-back: Task 34, the report's last text changes before the freeze (2026-10-30)

Order: `docs/work-orders/2026-10-30-task-34-last-text.md` (hq, Fable, 2026-10-30). The first version of the order
(one phrase only) was filed before hq rewrote it: `docs/work-orders/2026-10-30-task-34-other-uae-texts.md`; the
rewritten order supersedes it. Base `main` c4102b7, branch `task-34`. Opus 5.5, one session. USD 0.

**Limits:** report, README, report builder, KB manifest rows, datasheet, export, intent, site, tests. No model call,
nothing fetched, no chunks, nothing under `runs/`, `onyx/data/`, `eval/`, `kb/chunks/`, no gate, agent, prompt or key
file changed (`git diff --stat main -- runs onyx/data onyx/gate.py onyx/agents eval kb/chunks`: empty). Seven layers
(`engineering/_reference/llm-agents.md`): unchanged from Task 33; nothing shipped or deferred by this task. Owner of any
failure: Iyas.

## Summary

The report says "twenty-eight other UAE texts", names Mohammed Rawashdeh and Yanal Faouri, and its header gives the code
link plus one line for the knowledge base, demo video and replay site. eIDAS Art 8, COPPA 16 CFR 312.5 and Licence
3/2026 are VERIFIED manifest rows: 77 documents, 72 VERIFIED, 23 foreign, 32 UAE instruments. The README has the
Y.3172 clause 9 line, proved by a new test file. The report holds 5 pages at 2,192 words after six cuts, all ruled by
Iyas or the order.

## Decisions and rulings (Iyas, 2026-10-30, in session)

1. **The old pin test.** `test_a_typed_kb_count_that_differs_from_the_manifest_fails[fifteen other UAE laws]` swapped
   "twenty-seven other UAE laws"; it now swaps "...texts" (the same check on the new wording).
2. **A3, header.** The builder took exactly four header lines (the template's last is "GitHub link"). Ruling: keep the
   template's field name on the code link, "GitHub link (code)".
3. **A4, page fit.** After A1 to A3 and the order's cuts (a) to (c) the report was still 6 pages (5 lines, 405
   characters over). Ruling: (1) the header compressed to five lines, (2) S1's CPR 4.4 sentence, (3) gap 9's 106/2026
   clause, (4) gap 5 rewording only if still 6. Step (4) was not needed.
4. **Clause 9 wording** "the only outward call a run makes" approved: `kb.py` also downloads, but only in `kb fetch`.
5. **Licence 3/2026** row in (TDRA's own file, see C); "twenty-eight other UAE texts".
6. **Count pin** in `tests/test_kb.py` (outside the order's exempt files) moved to 77, 72, 3, 2, 23, 32.

Builder change for the five-line header: a header value may hold markdown bold (`_runs`, as body text does), so the
three labels on line 5 are bold in Word.

## Page count after each step (`scripts/report_pages.ps1`)

| step | pages | words |
|---|---|---|
| A1 to A3 (phrase, team, seven header lines) | 6 | 2,257 |
| cut (a) gap 12 NOTE clause | 6 | 2,239 |
| cut (b) gap 1 du clause | 6 | 2,228 |
| cut (c) Introduction sentence | 6 | 2,215 |
| ruling (1) header to five lines | 6 | 2,216 |
| ruling (2) S1 CPR 4.4 sentence | 6 | 2,203 |
| ruling (3) gap 9 106/2026 clause | **5** | 2,192 |
| Part C counts | **5** | 2,192 |

The register keeps every cut point: gap 12's NOTE sentence word for word (`docs/gaps.md`, `docs/site/gaps.html`,
README); du's chatbot channel (`docs/gaps.md` line 78, pinned by the row 1 test), the 106/2026 social-media scope (gap
9's searched clauses) and the CPR 4.4 expired-bundle candidate (`docs/gaps.md` line 602) in the register's own words.
The Introduction's "scored in both languages" sentence has no register line; README line 49 states Arabic parity.

## Part C, the three rows

| row | file | sha256 | publisher's own? |
|---|---|---|---|
| `eidas-910-2014-art8` | `kb/sources/global/eidas-910-2014-art8.txt` (3,379 bytes) | `fa53cfcb...` | yes: EUR-Lex HTML, CELEX 32014R0910, element #art_8, fetched 2026-10-21 |
| `coppa-16cfr312-5` | `kb/sources/global/coppa-16cfr312-5.txt` (9,146 bytes) | `f62f7bff...` | yes: eCFR versioner API, text of 2026-10-19, fetched 2026-10-22 |
| `licence-3-2026` | hq `standards-text/licence-3-2026-eitc-du-public-telecom-en-ar.pdf` (752,881 bytes, 47 pages) | `ccafd4ed...` | yes: tdra.gov.ae/-/media/About/LICENSING/EN/Licence-32026-EITC-Public.ashx (hq `telecom-law-and-licences-2026-10-17.md`); `licence-du-3-2026-en.pdf` is the same bytes |

All VERIFIED, binding; the two foreign rows are `extract`, "never a deciding clause", as the Task 31 rows; the licence
row copies Licence 2/2026's language and translation fields. No chunks for any (test).

## Done means

```
$ grep -c "other UAE laws" docs/report.md
0
$ grep -c "Saaydeh" docs/report.md README.md
docs/report.md:0
README.md:0
```

Links (`docs/report.md` lines 6 and 7, by Iyas's ruling (1) two lines, not four):

```
**GitHub link (code):** https://github.com/SHRA1M/onyx-hackathon-build (public from 2026-11-09)
**Knowledge base:** `kb/manifest.csv` and `kb/DATASHEET.md` in that repository. **Demo video:** `docs/video/mizan-demo.mp4` there (file lands 2026-11-08). **Replay site, no install:** https://shra1m.github.io/onyx-hackathon-build/site/
```

```
$ powershell -File scripts/report_pages.ps1
pages: 5
words: 2192
```

Count check, every number the report states (`build_report.check_kb_counts`, `check_values`):

```
documents report [77, 77]
verified report [72]
foreign report [23]
uae_other report [28]
manifest: documents 77 verified 72 foreign 23 uae_other 28
kb count failures []
value check failures []
```

```
$ python -m onyx kb verify
VERIFIED 72  REFERENCED 2  UNVERIFIED 3  HISTORICAL 0
  every fetched source matches its sha256
$ kb/DATASHEET.md: "77 manifest rows", "| VERIFIED | 72 |", "| UNVERIFIED | 3 |"
```

Full suite: `614 passed in 136.51s`. CI: see the PR.

```
$ sha256sum docs/report.md <hq>/report-draft-2026-10-23.md
518473ae285920381ae621e0341fa1318ccd15114fdbff71fac02998c89684e4  docs/report.md
518473ae285920381ae621e0341fa1318ccd15114fdbff71fac02998c89684e4  report-draft-2026-10-23.md
```

Before the copy the hq draft equalled `main:docs/report.md` byte for byte (`cmp`: no output). Backup:
`report-draft-2026-10-23.md.bak-2026-10-30-task-34` (`e1d6c4b2...`).

## Open questions for hq

- The eIDAS row holds Art 8 as adopted (2014); Regulation (EU) 2024/1183 amended eIDAS. Whether Art 8 changed was not
  checked (nothing fetched, per the Limits).
- The Introduction sentence "scored in both languages" is gone from the report and has no register line.
- The Pages URL waits on the submission-day check, as the order says.
