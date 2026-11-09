# Report-back: end-check order 3, the annex

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\end-check-order-3-annex-2026-11-08.md`, with both addenda and hq's answer to the second stop (option a). Branch `end-check-3-annex` from `main`. Commit `8adb4e9`. PR: https://github.com/SHRA1M/onyx-hackathon-build/pull/28 (not merged).

## The two stops, settled

1. Part 6's step (1) said "the two verdicts against the keys". The second addendum gave new words. Its four counts checked against `docs/annex.md` lines 279 to 293: five field-shape faults "listed for the fix after the shortlist" (S3-5, S5-5, S5-6, S4-3, S4-2), "6 checks in `onyx/gate.py`", "Two of these checks ... an unmatched word there ... was allowed", "the other four differences are listed for review": all match.
2. The 67 / 29 / 38 sentence failed `docs/build_report.py`'s value check inside the C3-tagged Result paragraph. hq: its own untagged paragraph after the table, before "Reading it". `build_report.py` unchanged.

## Checks before pasting

- 84 English-only chunks: 161 chunks, 77 with `text_ar`. Pass.
- The report's own words for the faults: per the second addendum (above). Pass.
- Retrieval paragraph (line 62) above the Next steps paragraph (line 109). Pass.
- Recount of `runs/ungoverned/` with `onyx/eval.py`'s claims rule (`run_metrics`), split by the team's pending proposal on the abstention step:
  ```
  runs 30; claims allowed 67; team-written (pending, abstention step) 29; model's own 38
  ```
- Line 28, "A bilingual embedder is listed under next steps": still true, through step (2), "the retrieval plan above".

## The five edits, each as it now stands in `docs/annex.md`

1. Retrieval paragraph, before "The model never sees the keys": **made**.
   > Two causes are named for the fix after the shortlist: a subscriber's chat line and the clause that answers it often share no words, and each chunk is embedded as bare clause text, without its document name or heading. The plan, in order: add that context to each chunk; measure a bilingual embedder (bge-m3, Qwen3-Embedding-0.6B) on held-out queries written by a teammate who has not read the chunks; only then re-record the scored runs.
2. "Next:" line replaced: **made** (line 109).
   > **Next steps, if shortlisted (2026-11-18 to the final on 2026-12-08).** None of this is built. In order: (1) fix the gate faults listed in Annex C: the five field-shape faults in the recorded verdicts against the keys, and the six exact-English-term checks, starting with the two that allow an unmatched word; review the other four verdict differences; (2) the retrieval plan above; (3) let the adviser read the whole conversation, so gaps 2 and 6 can be flagged where they arise; (4) re-record the scored runs once, so every figure moves together, and run the seven unseen scenarios cold in both languages; (5) widen the steered-subscriber test to 30 or more runs, with attackers who have not read the gate code; (6) for the live demo: a chat for the customer and a screen where staff take hand-overs and release holds, in Arabic and English, by text and then by voice; a question to the adviser at any step; routing for a step the scenario did not name (D-2); (7) Arabic text for the 84 English-only chunks, and the reviewer's code-level points.
3. Disclosure in "How the data is connected" (part 9, ruling 6, whole): **made** (line 57).
   > Each scored scenario also carries one proposal written by the team, not made by the model (`pending_proposal`): a move the law stops or the texts do not settle, put to the gate on purpose (S1 step 6, renewal without new consent; S2 step 5, hand-over timing; S3 step 3, the full record sent abroad; S4 step 5, suspension; S5 step 4, device block). At these five steps the key scores the adviser's gap flag, which is the model's. The two classification proposals (S1 step 1, S2 step 1) are plain code and logged as such; every other proposal in the scored runs is the model's.
   Step numbers match order 1's C.1 (S1 6, S2 5, S3 3, S4 5, S5 4).
4. Coordinator: **made**.
   - Line 56: "... Data Office 22, coordinator 8; the coordinator is code, not a model)."
   - Line 314: "the five manifests (four model-backed agents and the coordinator, which is code) in `mandates.json`".
5. Written-proposal split (part 9, ruling 5): **made**.
   - Own paragraph after the Result table (line 227):
     > Of the 67 such steps over the 30 ungoverned runs, 29 are the proposals the team wrote into the scenarios, each judged at its gap step, and 38 are the model's own.
   - "Reading it", replacing the old sentence:
     > But about two held-or-blocked steps go through per run, in both languages: about one is the proposal the team wrote into the scenario, and about 1.3 are the model's own (38 over 30 runs).

## Tests moved or added (no visible word changed by any)

- `tests/test_annex.py`: the mandates count pin follows the new line 56 text. New `test_the_written_proposal_split_matches_a_recount_of_the_ungoverned_runs` recounts the 30 runs and requires 30, 67, 29 and 38, and the sentence as its own paragraph.
- `tests/test_task_54.py`: `NEXT` is now the Next steps paragraph's bold lead. Annex A's last paragraph must start with it, and the old "Next:" line must be gone.

## Checks

`scripts/report_pages.ps1` (after `uv run python docs/build_report.py`):
```
pages: 5
words: 2577
annex starts on page: 6
total pages: 17
total words: 10179
```
The annex grew from 11 to 12 pages; the main text is unchanged.

Annex and report tests (`test_annex test_report test_task_45 test_task_51 test_task_51b test_task_53 test_task_54 test_site test_gaps`): `411 passed in 39.42s`.

Not run: the full suite; `docs/report.pdf` not rebuilt (not in the order).

## Open questions for hq

1. `docs/report.pdf` is now behind `docs/report.docx` (orders 2 and 3). Rebuild in a later order.
2. PRs #27 (order 2) and #28 (order 3) both rebuild `docs/report.docx` from `main`; whichever merges second needs the docx rebuilt after the merge.
