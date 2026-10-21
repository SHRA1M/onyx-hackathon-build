# Report-back: Task 8 Part C2b, and C3 stopped at S3, 2026-10-21

Orders: `docs/work-orders/2026-10-21-task-8-part-c2b.md`, then C3 of `docs/work-orders/2026-10-21-task-8-part-c.md`.
Built by Opus 5.5.

## C2b (commit bbc5497), no model calls

- Prompt v3 gap line, word for word as ordered (adviser only).
- `parse_output` collects register ids from an abstaining reply's notes (`gaps_in_notes`, exact id, not inside a
  longer word). The abstention records them when no `flag_gap` names a gap, with `gaps_source` "notes";
  otherwise "proposal". Eval has a "Gaps from notes" column, shown only.
- Replay: a log with no `gaps_source` on its abstentions replays without notes gaps (same pattern as C1).
- `eval/bakeoff.md`: the ordered line under the v2 table. Checked first: 10 of 10 Arabic v2 logs name the key's
  id in the adviser's notes.
- Checks: 8 new tests failed first, then passed, plus 1 bake-off test; 204 passed. check-data ok. selftest
  chain ok, replay matches. 112 committed logs replay to their verdicts. eval/scripted differs only by the
  new column (24 table lines, each the old line plus the column) and its 2 definition lines. The JSON is
  identical once the new field is removed.

## C3: stopped at S3 governed, by the 0.1 rule

Each scenario was recorded and then checked: running means against the v2 bake-off over the same scenarios.
After S3, Arabic citation validity was 0.87, against 1.00 in the bake-off.

| Row, S1 to S3 governed (en / ar) | Bake-off v2 | C3 v3 |
|---|---|---|
| Citation validity | 1.00 / 1.00 | 0.96 / 0.87 |
| Action recall | 0.70 / 0.52 | 0.70 / 0.72 |
| Obligation proxy | 0.25 / 0.37 | 0.40 / 0.37 |
| Gap recall | 0.44 / 0.00 | 0.78 / 0.78 |
| Abstention | 0.33 / 1.00 | 1.00 / 1.00 |

- Cause: 7 of the 9 failing proposals are Arabic `flag_gap` proposals with no clause and no quote (S1-6, S2-5 x3,
  S3-3 x3). v3 asked for these. Before v3 the same gaps sat in notes and were never scored as proposals.
  If citation-free `flag_gap` proposals are left out, Arabic citation validity is 1.00 and English 0.96.
  The other 2 failures are English model errors: S2-2 cited `tdra-cpr-v2-en:9.1`, which was not given, and
  S3-3 cited `pdpl-45-2021:22(1)` with a quote not in any chunk.
- Gaps from notes: 0 in all 18 runs. v3 moved the gaps into `flag_gap` proposals.
- Spend: C3 so far USD 1.61 (recorded USD 4.53 of 15). The rest of C3 is about 42 runs, about USD 3.7.
- Question for hq: should citation validity leave out `flag_gap` proposals that cite nothing (a gap is the
  absence of a clause)? Or should they count, and v3 also ask for the clause searched? Recording resumes with
  `--skip-existing` once hq decides. The 18 runs are kept.
