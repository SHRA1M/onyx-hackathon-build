# Report-back: Task 45, 11-04 sweep fixes

Order: `docs/work-orders/2026-11-04-task-45-sweep-fixes.md`. Stop file: `docs/report-back/2026-11-04-task-45-stop-1.md`.
Answers: `D:\Projects\hq\uni\ai-for-good-hackathon\task-45-stop-1-ruling-2026-11-04.md` (sha256 `42aa5807f688...`; hq
revised it during the build, and this is the version built). Branch `task-45`.

**Arabic: eye-checked by Iyas 2026-11-04.** All three WAM sentences match the WAM page.

## Summary

The register, README, report and annex now carry the 11-04 sweep: the five published criteria, the dated Gazette, csc
and PDPL lines, the agentic AI guide (through WAM) and the DoH standard as searched lines, and every count. Gap 6 and
gap 7's positions were rewritten in hq's words so they no longer contradict their own rows. Nothing scored moved.

## Done checks (order and ruling), each run

Output of the last run, after the ruling's final version was applied.

1. `grep -rn "four published" README.md docs/ tests/`, leaving out this task's order, report-backs and
   `tests/test_task_45.py` (which asserts the phrase is gone): prints nothing.
2. `grep -n "2026-11-04" README.md docs/gaps.md kb/manifest.csv kb/DATASHEET.md`: README 66 (Gazette), 73 (gap 3);
   gaps.md 13 (Gazette), 21 and 195 (gap 3), 318 (gap 5), 763 (gap 13), 794 (gap 14); manifest 42 (PDPL), 65 (csc),
   107 to 109 (the three rows); DATASHEET 120 (PDPL), 121 (csc), 126 (the guide).
3. `uv run python -m onyx kb verify`: "VERIFIED 100  REFERENCED 5  UNVERIFIED 3  HISTORICAL 0", "every fetched source
   matches its sha256".
4. Chunk check: `tests/test_task_45.py` finds every quote word for word in its chunk (three WAM, two DoH).
   `python -m onyx check-data`: "check-data ok: every quote verbatim, every rule cites a clause".
5. `python -m onyx gaps`, run twice: `docs/gaps.md` sha256 `22ad12d72e3b...` both times.
6. `uv run pytest -q`: 722 passed. Before: 8 of the new tests failed before any edit.
7. `scripts/report_pages.ps1`: pages 5, words 2373, annex starts on page 6, total pages 12, total words 6842.
   `scripts/report_pdf.ps1`: word pages 12, pdf pages 12, finds "Annex A", "Limits and next steps", "Annex F": True.
8. `git diff --stat kb/chunks/`: empty, because no committed chunk changed; `git status --short kb/chunks` shows only
   `doh-responsible-ai-standard-v1-2025.jsonl` and `wam-2026-08-21-agentic-ai-guide.jsonl`.
9. Ruling: `grep -rn "two emirate\|only UAE text setting" README.md docs/ onyx/ kb/ tests/`: nothing outside the Task 45
   order and report-backs.
10. `python -m onyx selftest`: "figures match a fresh eval of runs/". `git diff --stat -- runs eval onyx/data/keys
    onyx/data/rules.json onyx/data/mandates.json onyx/gate.py`: empty.

## Differs from the order

- `onyx/data.py`: one condition, so a file-quoted line marked `"chunked": true` counts as cited. hq: within the Limits.
- Item 8's last sentence had no target. hq replaced gap 6's and gap 7's whole positions instead.
- Item 8's two gap-7 `says` lines were replaced by hq's words: the DHA policy sets disclosure, not oversight, and the
  guide is not "the only UAE text".
- Item 2's csc wording was replaced by hq's whole note, which also absorbs the 2026-11-03 date.
- `tests/test_annex.py` and `tests/test_whatif.py` changed although they are outside the order's named tests. hq
  confirmed: both follow from items 10 and 3.
- WAM and guide rows share the instrument `agentic-ai-gov-guide`, which gives the order's 86. hq confirmed.
- No single-document `kb fetch` or `kb chunk` exists: the two documents were fetched alone and the two chunk files
  written with the kb's own writer. The WAM stealthy fetch was refused by the session's permission check; an ordinary
  browser fetch then worked. DoH: two fetches, the same sha256 `5e03adb73162...`, 490,537 bytes, 15 pages.

## Traps

A whole-kb `kb chunk` would delete both new chunk files: the chunker has no source spec for them, `consent` is not a
clause number, and `3.1.1.2.2` has too many parts for its pattern. A manifest changed only by `kb fetch` is never
committed.

## What this build may touch, and failure

Limits as the order's: text and three rows, read by hq as "nothing scored". It sends nothing outward except this PR. If
a check fails, the PR waits. Owner: Iyas.

## Merge danger

Two-way door: text and data, reverted by one revert. Blast radius: the public register and the counts a judge reads.

## Open

- Noted, not changed: `docs/annex.md:263`'s "none sets how an AI agent must behave with a consumer" is about the clauses
  listed just before it, which name neither the DHA policy nor the DoH standard, so it stays true. The ruling's new
  federal wording is in the register only.
- hq keeps one "done means" check for after this report.

## The number list, made before any edit (main 61e26e4, 2026-11-04)

Every number the report, annex, README, datasheet and site state about the knowledge base.

| File and line | States | Before | Order's after |
|---|---|---|---|
| `README.md:13` | manifest rows | 105 | 108 |
| `README.md:27` | VERIFIED, REFERENCED, UNVERIFIED | 98, 4, 3 | 100, 5, 3 |
| `README.md:30` | rows linking a landing page | 22 | not named; 22 expected |
| `docs/report.md:22` | "thirty other UAE texts" (UAE instruments less four) | thirty | **not named in the order**; thirty-two by the check in `docs/build_report.py` |
| `docs/report.md:24` | "thirty-eight foreign texts"; "98 are verified" | 38; 98 | 38; 100 |
| `docs/report.md:25` | "two unpublished texts and one unreachable one" | 3 | 3 |
| `docs/report.md:43` | "holds 105 documents" | 105 | 108 |
| `docs/report.md:52` | "SRC-2 105 documents" | 105 | 108 |
| `docs/report.md:131` | "the 34 UAE instruments" | 34 | 36 |
| `docs/annex.md:27` | documents; UAE instruments | 105; 34 | 108; 36 |
| `docs/annex.md:28` | names "the DHA AI policy and the UAE AI Charter" | | names DHA, DoH, Charter |
| `docs/annex.md:29` | web pages; announcements; news report; free-zone; ITU; foreign | 3; two; 1; 3; 6; 38 | 3; three; 1; 3; 6; 38 |
| `docs/annex.md:32-33` | VERIFIED, REFERENCED, UNVERIFIED | 98, 4, 3 | 100, 5, 3 |
| `docs/annex.md:45` | committed chunks, documents | 156, 19 | what the new chunks make: 161, 21 |
| `docs/annex.md`, "chunks with `text_ar`" | chunks holding Arabic | read from chunks | **not named in the order**; moves by the three WAM chunks |
| `kb/DATASHEET.md:7` (generated) | rows, instruments | 105, 84 | 108, 86 |
| `kb/DATASHEET.md:11-13` (generated) | status counts | 98, 4, 3 | 100, 5, 3 |
| `kb/DATASHEET.md:82` (generated) | license_note rows | 105 | 108 |
| `kb/DATASHEET.md:86` (generated) | rows; cited clauses; documents | 105; 156; 19 | 108; 161; 21 |
| `kb/DATASHEET.md:18-37` (generated) | binding, jurisdiction, language rows | 57 UAE of 105 | follow the manifest |
| `docs/site/index.html:114`, `docs/site/kb.html:90` (generated) | documents, VERIFIED, REFERENCED, UNVERIFIED | 105, 98, 4, 3 | 108, 100, 5, 3 |
| `kb/export/InputDocs/Inputs.md:7,55` (generated) | UAE_Binding, UAE_Advisory files | 43, 11 | **not named in the order**; 44, 13 |
| `tests/test_kb.py:402,534,607,656` | pins | 105, 98, 4, 3, 34 | 108, 100, 5, 3, 36 |
| `tests/test_report.py:387-389,397` | pins | 105, 98, thirty, 34 | 108, 100, thirty-two, 36 |
| `tests/test_annex.py:123-125,141-150` | pins | 105, 98, 34, two announcements | 108, 100, 36, three |

Not a knowledge-base number, left alone: `docs/report.md:122` "156 calls" (model calls, governed runs).

## CI

PR #14, https://github.com/SHRA1M/onyx-hackathon-build/pull/14. "reproduce" on commit `cc2d718`: passed on the push (run 41852945958, 1m35s) and on the pull request (run 41852958452). The PR is not merged.
