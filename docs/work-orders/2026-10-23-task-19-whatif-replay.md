# Order: Task 19, what-if replay under a proposed rule (hq, Fable, 2026-10-23)

Build model: Opus 5.5. No model calls; USD 0. Starts after the Task 18 report-back is accepted by hq, from its commit
with CI green. Copy this file into `docs/work-orders/2026-10-23-task-19-whatif-replay.md` first. Nothing here changes
`onyx/gate.py`, `onyx/data/rules.json`, `onyx/data/keys/`, `onyx/data/mandates.json`, `onyx/eval.py`,
`onyx/selftest.py`, `onyx/runs.py`, `kb/`, `onyx/data/gaps.json`, any committed run or any figure in
`eval/results.md`. Sources allowed: this repo and the hq file `competitor-code-read-2026-10-23.md` section 5 if a
reason is needed; nothing from memory or the web.

Why: Mizan finds a gap and recommends a rule; it does not test the rule. A competitor's design (not running) proposes a
repair, replays the same incident under it and records what the repair fails to fix. Our `replay` already re-decides a
recorded run offline from the logged model responses, so the same demonstration costs one wrapper around the frozen
gate and no model call. On the recorded S2 run it shows two changes and one new finding, all computable today.

## The proposed rule (data, never loaded by the gate)

`onyx/data/proposed/gap-1.json`:

```json
{
  "id": "proposed-gap-1",
  "gap": "gap-1",
  "status": "proposed, not law",
  "addressee": "TDRA",
  "text_en": "When a conversation on an automated channel becomes a Consumer Complaint (CPR 2.1.7), the non-human agent stops and a named trained human (licence 9.1) takes the conversation within two minutes of the trigger; the hand-over moment is recorded and is the start of the T1(2a) measurement.",
  "text_ar": "عند تحوّل محادثة على قناة آلية إلى شكوى مستهلك (المادة 2.1.7 من لائحة حماية المستهلك)، يتوقف الوكيل غير البشري ويتولى المحادثة موظف مدرّب مُسمّى (المادة 9.1 من الرخصة) في غضون دقيقتين من لحظة الشكوى؛ وتُسجَّل لحظة التحويل وتكون بداية قياس T1(2a).",
  "value": "2",
  "unit": "minutes",
  "value_basis": "qos-v3-0-t1-2a: the only hand-over time the texts measure (indicative, after the IVR choice); the number is TDRA's to set",
  "trigger_fact": "grievance_expressed",
  "adds_deadline_to": "cpr-26-7-2",
  "answers": {"verb": "route", "mark": "within_time"},
  "requires_record": "hand-over time"
}
```

The Arabic is hq's wording; Iyas checks it in the file before publication. If the JSON needs another field to work, add
it and say so in the report-back; do not change the texts.

## Items

1. **Module `onyx/whatif.py`.** `replay_under(path, rule_id=None) -> (recorded, whatif, changes)`.
   - Builds the `Coordinator` exactly as `runs.replay` does (same arguments, same `RecordedModel` and
     `RecordedRetriever`, same chain check: a broken chain is never replayed), then sets `run.decide` and
     `run.decide_pending` to the two wrappers below. `runs.py` is not edited; if you must share code, copy the few lines.
   - `decide_under(rule)`: calls `gate.decide`. If the verdict's reasons hold an obligation whose `clause` is
     `rule["adds_deadline_to"]` and `state.facts[rule["trigger_fact"]]` is yes, append one reason:
     `{"gate": "proposed-gap-1", "kind": "obligation", "proposed": true, "text": "hand over within 2 minutes of
     <facts time> (proposed-gap-1, not law)", "deadline": {"rule": "proposed-gap-1", "value": "2", "unit": "minutes",
     "from": <facts time>}}`. The verdict and `clause_ids` are unchanged.
   - `decide_pending_under(rule)`: calls `gate.decide_pending`. Only when the verdict is `hold`, every reason of kind
     `check` has `gate == "deny_by_default"`, `proposal.verb == rule["answers"]["verb"]` and
     `proposal.args.get("mark") == rule["answers"]["mark"]`: return `allow`, `clause_ids` unchanged (the proposed id
     is never a `clause_ids` entry; it appears in reasons only, like a design basis), reasons = the original reasons
     plus `{"gate": "proposed-gap-1", "kind": "check", "proposed": true, "text": "the proposed rule answers the step's
     question: <text_en>"}` plus, when the log carries no time fact at the hand-over step
     (`answers` step `handover_step` + 1, here S2-4), `{"gate": "proposed-gap-1", "kind": "finding", "proposed": true,
     "text": "second-order: the rule needs the hand-over time recorded; this run records the trigger at <time> and no
     hand-over time, so the two-minute condition cannot be checked"}`. Any other hold, and every block, is returned as
     the gate gave it.
   - `changes`: one row per decision whose verdict or reasons differ: `(entity_id, verb, recorded verdict, what-if
     verdict, added reasons)`. With `rule_id=None` the wrappers are not installed and the result equals `runs.replay`.
2. **Page `docs/replay/whatif-S2-gap-1.md`**, written by the module from `runs/c5/S2/run1.jsonl`: title; the run and
   its chain result; the rule's `text_en` and `text_ar` under the heading "Proposed rule, not law"; `value_basis`; a
   table "What changes" from `changes`; "What stays": "N of M decisions identical"; "Second-order finding" with the
   finding text; one closing line: "Generated by `python -m onyx whatif`; the gate, keys and committed runs are
   unchanged; this page is a what-if, not a result." `docs/replay/index.html` gets one entry, text "What-if: S2 under the
   rule gap 1 recommends", wherever the viewer lists the five scenarios: a link to the page if the index links, a nav
   entry that opens the page's text if the viewer embeds its pages. Keep every existing replay-viewer test passing;
   if one asserts the exact scenario list, extend it.
3. **CLI** `python -m onyx whatif <log> [--rule gap-1] [--out docs/replay]`, registered in `onyx/__main__.py` like
   the others. Without `--rule` it prints "no rule: equals replay" and the equality result. With the rule it prints the
   changes table and writes the page.
4. **README**, two sentences at the end of the paragraph that introduces the gap register (the one naming `docs/gaps.md`):
   "Gap 1 is also tested, not only stated: `uv run python -m onyx whatif runs/c5/S2/run1.jsonl --rule gap-1` replays the
   recorded S2 run under the rule the register recommends (proposed, not law): the held step S2-5 is released, the
   hand-over duty gains a two-minute clock, and one new finding appears: the rule needs the hand-over time recorded,
   which this log does not carry. Page: `docs/replay/whatif-S2-gap-1.md`." In the "For the reviewer" block, line 2
   gains at its end: "; `docs/replay/whatif-S2-gap-1.md` tests gap 1's recommended rule by replay".
5. **Report `docs/report.md`**, S2 paragraph: replace "How fast must a chat hand over? No text: gap 1." with "How fast
   must a chat hand over? No text: gap 1. Replayed under the rule the register recommends, the held step releases, the
   hand-over duty gains its clock, and a new finding appears: the hand-over time must be recorded
   (`docs/replay/whatif-S2-gap-1.md`)." Rebuild the docx; the value check must pass unchanged (no tagged figure is
   touched). Run `scripts/report_pages.ps1`. Five or fewer: record pages and words. Six: apply the Task 18 ladder one
   step at a time from the first unused step, recount after each, record the steps used; if the ladder reaches its
   step 5, stop and report. hq aligns `report-draft-2026-10-23.md` to the repo text afterwards; do not edit hq files.
6. **Arabic run.** Run the module on `runs/c5/S2/ar/run1.jsonl` with the rule and report whether the same two decisions
   change and the same finding appears. No page for it.
7. **Tests fail first then pass:**
   a. `onyx/data/proposed/gap-1.json` loads; `gate.Knowledge.load().rules` has 109 ids and none starts with
      `proposed-`; `data.load_rules()` is unchanged.
   b. `whatif.replay_under(path)` with no rule equals `runs.replay(path)` on `runs/c5/S2/run1.jsonl`.
   c. With `gap-1` on that run: exactly two decisions change: `S2-3-care` `draft_reply`, verdict `block` unchanged,
      one added obligation reason with `proposed: true`; `S2-5-coordinator` `route` (pending), `hold` to `allow`,
      with one added check and one added finding, both `proposed: true`. Every other decision equal. If the run shows
      a third change, stop and report it; do not widen the test.
   d. A hold whose reasons include any check not from `deny_by_default` is never released (unit test with a made-up
      verdict).
   e. The page and the README contain "proposed, not law"; the index links the page.
   f. `git diff --stat <Task 18 commit>..HEAD -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json
      onyx/eval.py onyx/selftest.py onyx/runs.py kb runs onyx/data/gaps.json eval/results.md` prints nothing; paste
      the empty output in the report-back.
   Full suite, CI green, commit, push. Report under 12 lines to `docs/report-back/2026-10-2X-task-19-whatif-replay.md`:
   the changes table for both runs, pages and words after item 5, ladder steps used, test count, the item 7f output.

## Stop and ask when

- The S2 run's step-5 hold carries any reason other than `deny_by_default` and the design basis.
- A third decision changes under the rule, in either language.
- The replay-equality tests fail anywhere after your change.
- The five-page check reaches ladder step 5.
- Anything would change a file in the first paragraph's list.
