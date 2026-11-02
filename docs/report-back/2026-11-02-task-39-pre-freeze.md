# Report-back: Task 39, pre-freeze changes (2026-11-02, Opus, in progress)

Order: `docs/work-orders/2026-11-02-task-39-pre-freeze.md` (hq's `task-39-pre-freeze-order-2026-11-02.md`). Iyas
confirmed A, B, C and D; E is skipped until he says (not built, Iyas's call).

## State

| Item | State | Commit |
|---|---|---|
| A | Built, pushed, CI on PR #13 green | `67e6792` |
| B | Stopped (stop 1 below). No code written yet | |
| C | Built, committed, not pushed | `19278f9` |
| D | Stopped (stop 2 below). Nothing written | |
| E | Not built, Iyas's call | |

## Done means so far

1. A: `grep -c "17 verbs" docs/annex.md` -> `0`. `report_pages.ps1` -> `pages: 5` / `words: 2366` /
   `annex starts on page: 6` / `total pages: 10` / `total words: 5011`. `report_pdf.ps1` -> `word pages: 10` /
   `pdf pages: 10` / `pdf finds 'Annex A': True`. `uv run pytest` -> `661 passed`. PR #13 checks: `reproduce pass`
   (runs 41431622886 and 41431629562). hq copy `report-annex-2026-11-02.md` equals `docs/annex.md` (sha256
   `956a102b1d38a141...` both); text v3 reads "the 16 verbs (16: repo count, Task 39)".
3. C: the table is in `README.md` under "For the reviewer"; each command run once, first line:
   - `uv run python -m onyx kb verify` -> `VERIFIED 83  REFERENCED 2  UNVERIFIED 3  HISTORICAL 0`
   - `uv run python -m onyx why runs/c5/S2/run1.jsonl --step 3` -> `S2 step 3 (S2-3), runs/c5/S2/run1.jsonl`
   - `uv run python -m onyx selftest` -> `Selftest: S1 Roaming before a flight (en, governed). SYNTHETIC operator and subscriber.`
   - row 4 is a link to `#y3172-mapping` (the README's "Y.3172 mapping" heading).
   New test `test_the_reviewer_table_names_only_commands_and_paths_that_exist`; two tests that pinned the numbered
   lines now read the table rows (`tests/test_report.py`, `tests/test_site.py`). Both fail on the old README, pass
   on the new. README, report, site and gaps tests: `191 passed`.

## Stop 1 (item B): must-cite clauses never shown, at steps that scored a hit

The order: stop when "the key-clause row shows a step whose must-cite clause was never shown to the model in a run
that still scored a hit (name it: that is a finding, not a bug to hide)". A probe over the C5 logs (the order's
counting, before any code) shows this in every scenario:

| Lang | Shown of total | By mandate | Only by retrieval | Clause-instances not shown at a step that hit | Steps |
|---|---|---|---|---|---|
| en | 186 of 234 | 160 | 26 | 43 | S1-6, S2-5, S2-6, S3-3, S4-4, S4-5, S5-4 |
| ar | 166 of 234 | 160 | 6 | 68 | S1-6, S2-5, S2-6, S3-1, S3-3, S4-4, S4-5, S5-4 |

"Hit" is action recall: the key's agent proposed the key's verb to the right addressee. Examples, the same in both
runs: S2-5 (adviser, the abstention step) was never shown `cpr-26-7-1`, `qos-v3-0-t1-2a`, `licence-9-1`,
`cpr-26-4-5`; S5-4 never `cpr-24-10`, `et-33`; S4-5 never `pdpl-18-1`, `pdpl-21-2-a`, `cabinet-66-2023-34-1`,
`cpr-22-2`. What it likely means (not checked further): a key's `must_cite` lists the clauses the step's record must
carry, many of which the gate adds to its verdict; an action hit needs the right verb, not those clauses in the
prompt. So "shown" is low where the gate, not the model, carries the law.

Two counting choices the order leaves open, taken in the probe:
- Steps where no agent sent a prompt (S1-1 and S2-1, plain-code steps, 3 must-cite each) are left out of the total,
  as `must-cite given` does. Counting them adds 12 per language, all not shown.
- Each `must_cite` entry counts once, mapped to its chunk; two rules on one chunk count twice (S3-3:
  `pdpl-13-2-d` and `pdpl-13-2-g` are both `pdpl-45-2021-en:13(1)`).

Questions for hq:
1. Build the row and the annex sentence as ordered, with the finding named in the report-back only? Or add words
   to the annex sentence (for example "the rest are carried by the gate's verdict")? The sentence as ordered would
   read, from the probe: "186 of 234 ... in English and 166 of 234 in Arabic; 160 of 234 came from the mandate list
   alone, which is the English-centred retriever at work, and why the mandate list comes first." (Arabic
   retrieval-only 6 is below English 26, so the clause applies.) Note "160 of 234 from the mandate alone" is the
   same in both languages: the mandate list does not depend on the language.
2. Keep the two counting choices above?

## Stop 2 (item D): the C5 hand-over latency cells

The order: stop when "a C5 hand-over latency cell is not a number". From `eval/results.json`,
`c5.C5.by_scenario.*.handover_latency_steps`:

```
S1 en None  ar None
S2 en 0.0   ar 0.0
S3 en None  ar None
S4 en 0.0   ar 0.0
S5 en 0.0   ar 0.0
```

S1 and S3 have no `handover_step` in their keys, so they have no latency. Second point: `eval/results.md` does not
print a C5 hand-over latency at all. The only "Hand-over latency (steps)" column is in the Governed table, which is
C3 (prompt v3, `runs/S*`): `n/a` for S1 and S3, `0` for S2, S4, S5.

Questions for hq:
3. Write "is 0 steps in every scored run of the three scenarios with a hand-over (S2, S4, S5)"? Or another wording?
4. The sentence points at "the hand-over latency row in `eval/results.md`". Point it at the C3 Governed column
   (same values), or have B's eval change also print the C5 hand-over latency per scenario and language in
   `eval/results.md`, so the pointer names C5?

## Limits kept so far

No run, no model call, no fetch, no spend. No figure, gap, rule, key, prompt, gate, mandate or scenario changed.
Failure mode: closed; only `task-36` pushed (A), nothing merged, no tag.
