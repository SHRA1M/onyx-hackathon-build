# Task 8 Part C4 addendum, 2026-10-21 (hq, Fable, after the S1 stop)

hq read the 4 C4 S1 logs (17a1f14). The stop was right. Both English runs fail S1 step 3 on
`cabinet-56-2024:5(6)`, the clause id without its `-en` ending; the clause was in care's prompt and the quote is
verbatim. C3 had the same slip twice (`pdpl-45-2021:22(1)`, `cabinet-66-2023:34(5)`). Four in 341 citations is a
pattern. The ending is a naming convention of our KB, not law, and the ids shown to the model are inconsistent
(`licence-2-2026:9.1` carries no ending; `cabinet-56-2024-en:5(6)` does).

Decision (hq, Fable, 2026-10-21): resolve the id in a bounded way. No prompt change; v4 stands; the 4 S1 runs
count. Copy this file into `docs/work-orders/`.

## Items, before any further model call

1. **Resolution rule**, one function used by the gate and by the eval: a cited id that is not among the clauses
   given to that agent for that step resolves to the given clause whose id is equal after the language ending
   (`-en` or `-ar`) is removed from the document part of both ids, and only when exactly one given clause matches.
   Never against the whole KB, never fuzzy, never when two match. The gate event records `cited` and `resolved`
   for every corrected id.
2. **Replay**: logs recorded before this change replay as recorded (the C1 and C2b pattern); their gate verdicts
   do not change. The eval applies the rule to every log when it scores citation validity, so the 4 S1 logs and
   the C3 logs are rescored. `eval/results.md` shows C3 citation validity both ways with the line: "Clause-id
   resolution added 2026-10-21 (hq, after C4 S1): an id missing its language ending resolves to the one given
   clause it names; 4 of 341 citations across C3 and C4 S1." The bake-off tables keep the old rule, byte-identical.
3. **Tests fail first, then pass**: `cabinet-56-2024:5(6)` with 5(6) given resolves and the citation is valid;
   the same id with 5(6) not given stays invalid; an id that matches two given clauses stays invalid; an exact id
   is untouched. Full suite, check-data, selftest, eval twice byte-identical. Commit.
4. **README "Model" section**: one sentence stating the rule and the count, dated.
5. **Resume** S2 to S5 governed, 2 runs per cell, on prompt v4, only if S1 English citation validity under the new
   scoring is within 0.1 of C3. All caps and stop rules in the C4 order hold: C4 USD 6.00, recorded total USD
   14.50, the 0.1 rule after every scenario (both sides scored under the new rule).
6. Push after the batch ends, with the C4 report as the order says, plus one line: how many ids were resolved in
   C4 and on which steps.

## Stop and ask when

As in the C4 order. Also: if the resolution rule would need to touch `kb/`, `rules.json` or the keys, or if S1
English fails item 5.
