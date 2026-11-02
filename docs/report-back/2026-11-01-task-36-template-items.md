# Task 36 report-back: ITU's template items (written 2026-11-02, Opus)

Order: `docs/work-orders/2026-11-01-task-36-template-items.md`, branch `task-36`. hq rulings followed: stop 1 (cuts 1
and 2), stop 2 (`D:\Projects\hq\uni\ai-for-good-hackathon\task-36-stop-2-ruling-2026-11-01.md`), stop 3 (one pinned
test string, Iyas carried the answer 2026-11-01). Stops filed: `2026-11-01-task-36-stop-2.md`, `2026-11-01-task-36-stop-3.md`.

## What was built

1. Report headings in the template's order, with the new sections Role of AI, Requirements (three ranked groups),
   Demo scenarios and the gaps method paragraph. Final text is hq's stop-2 file, copied byte for byte.
2. `python -m onyx why <log> --step <n> [--lang ar]`: reads the committed log only, no model call.
3. `onyx/data/proposed/gap-4.json` (UAE Data Office; Arabic marked as the team's translation, not eye-checked) and
   `docs/replay/whatif-S4-gap-4.md`.
4. Builder: a 4 pt spacer after each table, figures 11 cm. README: the four demo steps as one list, and `why` added
   to the keyless commands (so `tests/test_cli.py` runs it on every suite). Site `verify.html`: one `onyx why` line.
   hq copy `report-draft-2026-10-23.md` replaced (same sha256 as `docs/report.md`). CHANGELOG entry 2026-11-02.

## Differs from the order

- The order cut the report by cuts 1 to 4 and hq's rulings. Getting to 5 pages also took hq's stop-2 layout changes
  and ten text changes. No gap row, scenario, figure, clause or addressee was cut.
- Two tests follow the ruled text: the figure width, now `Cm(11)` (stop 2), and the Results sentence (stop 3).

## Mapping check (item 1.5), row by row

The Readiness cell names a dimension other than data and model handling on every row where one applies:
SRC 11 (AI for Inclusion); C 7 (Strategy Alignment); PP 10 (AI & Policies, a policies dimension); M 6 (Human Interface);
P 8 (Collaboration with AI); D 6 (Human Interface); SINK 10 (AI & Policies); MLFO and ML sandbox cite factors
(Standards, Sandbox). No row is empty, so nothing was added.

## Checks

1. `scripts/report_pages.ps1`:

```
pages: 5
words: 2346
```

2. `docs/build_report.py` passes its count and value checks (exits on any failure; printed `docs/report.docx`). Two builds byte-identical. Files changed against `main`, all Task 36:

```
CHANGELOG.md
README.md
docs/build_report.py
docs/replay/whatif-S4-gap-4.md
docs/report-back/2026-11-01-task-36-stop-2.md
docs/report-back/2026-11-01-task-36-stop-3.md
docs/report.docx
docs/report.md
docs/site/verify.html
docs/work-orders/2026-11-01-task-36-template-items.md
onyx-hackathon-build-archive.md
onyx-hackathon-build-background.md
onyx-hackathon-build-workingBrief.md
onyx/__main__.py
onyx/data/proposed/gap-4.json
onyx/site.py
onyx/whatif.py
onyx/why.py
tests/test_report.py
tests/test_whatif.py
tests/test_why.py
```

3. python-docx on `docs/report.docx`:

```
tables: 2 empty paragraphs after tables: 2
 line=80 rule=exact before=0 after=0 run sz(half-pt)=['8']
 line=80 rule=exact before=0 after=0 run sz(half-pt)=['8']
picture width: 3960000 == Cm(11): True
picture width: 3960000 == Cm(11): True
```

4. `grep -c "Global example" docs/report.md`: 0; `grep -c "| 7 |" docs/report.md`: 0.

5. Full suite: `643 passed in 126.14s (0:02:06)` (641 at stop 2, plus the `why` keyless-command test). CI: `reproduce` green on the push (run 41411835132) and on PR #13 (run 41411868648).

6. Headings in `docs/report.md`, in order:

```
## Introduction
## Description of the use case
## What is the role played by AI?
## Requirements
## Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies
## Demo scenarios
## Error scenarios
## Policy gaps and standards gaps derived from the mapping exercise
## Limits and next steps
```

7. Selftest: C5 figures unchanged from Task 35b (`eval/results.md`: action recall 0.96 / 1.00, citation validity 0.99 / 1.00; selftest ends "figures match a fresh eval of runs/"). No diff in `eval/`, `runs/`, `onyx/data/` keys, prompts, rules or mandates; no run, no API call.

8. `uv run python -m onyx whatif runs/c5/S4/run1.jsonl --rule gap-4`:

```
  S4-5-care          propose_change hold -> hold  + obligation, finding (proposed)
9 of 10 decisions identical
docs/replay/whatif-S4-gap-4.md
```

9. `uv run python -m onyx why runs/c5/S3/run1.jsonl --step 3`:

```
S3 step 3 (S3-3), runs/c5/S3/run1.jsonl
From the committed log only; no model call. Operator, subscribers and numbers are synthetic.

S3-3-adviser  flag_gap  verdict: allow
  event hash 3e5369c8a39839d273c317e4d289ff975053d0f07dbaae3bee31845414fb622b

S3-3  abstain  verdict: insufficient_evidence
  event hash 8e26100c937fc89a66e6100e85364a74ae3b7ff3a76d9e5037bfaeb8943c98d2
  PDPL 22, PDPL 23(1)(a), PDPL 23(2), PDPL 22(1), CPR 4.4.1, CPR 4.22.4, Child Digital Safety 7(1), PDPL 6(1)(b), CPR 24.10, ET 33

S3-3-care  draft_reply  verdict: block
  event hash 8eb4f048fe316fec932a1a6f9d9987f7522cd0ef97da7e5be0bcc4019304ef1f
  clause PDPL 22 (pdpl-22), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 25 [binding, UAE]
    "Personal Data may be transferred to outside of the State in the following cases approved by the Bureau"
  clause PDPL 22(1) (pdpl-22-1), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 25 [binding, UAE]
    "The State or Province to which the Personal Data is transferred shall have legislations addressing Personal Data Protection"
  clause PDPL 23(2) (pdpl-23-2), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 26 [binding, UAE]
    "The Executive Regulations of this Decree by Law set forth the controls and stipulations referred to in Paragraphs (1) of this Article, which should be observed during the transfer of data outside the State."
  clause PDPL 23(1)(a) (pdpl-23-1-a), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 25 [binding, UAE]
    "may transfer data under a contract or agreement obligating the companies in such countries to adopt measures, controls and requirements set out in this Decree by Law"
  clause PDPL 8(1) (pdpl-8-1), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 11 [binding, UAE]
    "Carry out the processing in accordance with the instructions of the Controller and contracts and agreements concluded between them"
  clause PDPL 13(2)(d) (pdpl-13-2-d), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 17 [binding, UAE]
    "The targeted sectors or establishments with whom its personal data will be shared from inside and outside the State."
  clause PDPL 13(2)(g) (pdpl-13-2-g), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 17 [binding, UAE]
    "Protection measures for cross-border processing carried out in accordance with Articles (22) and (23)"
  clause Licence 3.4.1 (licence-3-4-1), Public Telecommunications Licence No. 2/2026 (e&), term 2026-08-09 to 2046-08-08, bilingual, p. 11 [binding, UAE]
    "the Licensee shall continue to be fully liable for any obligations set out in this License"
  clause Telecom Law 72(2) (telecom-law-72-2), Federal Law by Decree No. 3 of 2003 Regulating the Telecommunications Sector, consolidated (portal, last update 27 Sep 2020), p. 26 [binding, UAE]
    "Illegally copies, discloses, or distributes the content of a telephone call or text message or any of the telecommunications services"
S3-3-care  override_refused by Human agent H-02 (synthetic): block, the verdict stands
  event hash cbfad398cafef58475775b755df341200099d65005977df7223f58e2546636bc
```

10. `--lang ar`:

```
S3 الخطوة 3 (S3-3), runs/c5/S3/run1.jsonl
من السجل المعتمد فقط؛ دون استدعاء نموذج. المشغّل والمشتركون والأرقام اصطناعية. (العناوين ترجمة الفريق، لم تُراجع بالعين)

S3-3-adviser  flag_gap  القرار: allow / سماح
  بصمة الحدث 3e5369c8a39839d273c317e4d289ff975053d0f07dbaae3bee31845414fb622b

S3-3  abstain  القرار: insufficient_evidence / أدلة غير كافية
  بصمة الحدث 8e26100c937fc89a66e6100e85364a74ae3b7ff3a76d9e5037bfaeb8943c98d2
  PDPL 22, PDPL 23(1)(a), PDPL 23(2), PDPL 22(1), CPR 4.4.1, CPR 4.22.4, Child Digital Safety 7(1), PDPL 6(1)(b), CPR 24.10, ET 33

S3-3-care  draft_reply  القرار: block / منع
  بصمة الحدث 8eb4f048fe316fec932a1a6f9d9987f7522cd0ef97da7e5be0bcc4019304ef1f
  البند PDPL 22 (pdpl-22), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 25 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "Personal Data may be transferred to outside of the State in the following cases approved by the Bureau"
  البند PDPL 22(1) (pdpl-22-1), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 25 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "The State or Province to which the Personal Data is transferred shall have legislations addressing Personal Data Protection"
  البند PDPL 23(2) (pdpl-23-2), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 26 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "The Executive Regulations of this Decree by Law set forth the controls and stipulations referred to in Paragraphs (1) of this Article, which should be observed during the transfer of data outside the State."
  البند PDPL 23(1)(a) (pdpl-23-1-a), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 25 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "may transfer data under a contract or agreement obligating the companies in such countries to adopt measures, controls and requirements set out in this Decree by Law"
  البند PDPL 8(1) (pdpl-8-1), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 11 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "Carry out the processing in accordance with the instructions of the Controller and contracts and agreements concluded between them"
  البند PDPL 13(2)(d) (pdpl-13-2-d), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 17 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "The targeted sectors or establishments with whom its personal data will be shared from inside and outside the State."
  البند PDPL 13(2)(g) (pdpl-13-2-g), Federal Decree-Law No. 45 of 2021 Concerning the Protection of Personal Data (PDPL), p. 17 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "Protection measures for cross-border processing carried out in accordance with Articles (22) and (23)"
  البند Licence 3.4.1 (licence-3-4-1), Public Telecommunications Licence No. 2/2026 (e&), term 2026-08-09 to 2046-08-08, bilingual, p. 11 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "the Licensee shall continue to be fully liable for any obligations set out in this License"
  البند Telecom Law 72(2) (telecom-law-72-2), Federal Law by Decree No. 3 of 2003 Regulating the Telecommunications Sector, consolidated (portal, last update 27 Sep 2020), p. 26 [binding, UAE]
    لا يحمل المقطع المعتمد نصاً عربياً لهذا البند؛ النص الإنجليزي:
    "Illegally copies, discloses, or distributes the content of a telephone call or text message or any of the telecommunications services"
S3-3-care  override_refused من Human agent H-02 (synthetic): block / منع, القرار قائم
  بصمة الحدث cbfad398cafef58475775b755df341200099d65005977df7223f58e2546636bc
```

11. Not run: Iyas opens `docs/report.docx` once to confirm page 5 ends with "Limits and next steps" and there is no page 6.

## Open questions for hq

1. The `why` output in Arabic gives the English quote for the PDPL clauses: the committed chunks carry no Arabic text for them, and the tool says so on each clause. Leave it, or add the Arabic PDPL chunks in a later order?
2. Carried: in-force dates (Maine, India TCCRR, Korea Art 31); the Saudi Arabic eye-check; GitHub Pages on submission day.
