# Task 29: what Mizan takes from the field (order, Fable, 2026-10-29)

Build runs on Opus in `D:\Projects\engineering\onyx-hackathon-build`, from `main` at df7c29c (CI green), on a
branch `task-29`. Ruling behind every line: `fable-take-ruling-2026-10-29.md`. Four parts, A to D, in that order;
one PR per part, CI green before the next starts. Submission 2026-11-09; this order must be merged by 2026-11-03 so
the video can start.

> **For agentic workers:** use superpowers:executing-plans (native) or subagent-driven-development to run this
> part by part. Steps use `- [ ]` boxes. A building session builds the order and does not re-decide it.

**Goal:** four additions a judge can see, all computed from what is already committed, USD 0 in model calls: a
model-down error scenario on the recorded S2 run; the expected / found / missed / unexpected gap table and 95%
intervals in `eval`; binding labels on every cite and a KB datasheet; gap-12 reworded to map before it claims.

## Only these sources

| Source | File (under `D:\Projects\hq\uni\ai-for-good-hackathon\`) |
|---|---|
| The ruling, with the "check" findings and the not-taken list | `fable-take-ruling-2026-10-29.md` |
| Earlier constraints that still bind (sources table, global constraints, addenda 13 to 31) | `work-order-2026-10-17.md` |
| Gap-12 row text, metrics and quotes | `agentic-readiness-ruling-2026-10-26.md` sections 2 to 4 |
| ITU's words that item D quotes | `itu-design-feedback-2026-10-28.md` |
| Report text as merged | `report-draft-2026-10-23.md` (byte-identical to `docs/report.md`) |
| Wilson interval | the standard formula; no library, write the ten lines in `eval.py` with a docstring and a test against two known values |

Ideas from any entry, code from none (Iyas, 2026-10-22). No rival repo is opened by the build.

## Global constraints (added to the 10-17 order's)

- **USD 0.** No live model call in this task. `record` is not run. If a step seems to need one, stop and ask.
- **Logs untouched.** No file under `runs/` changes. Every C3, C4 and C5 log must replay as recorded after every part
  (the existing replay tests prove it; CI runs them).
- **Keys untouched** (`onyx/data/keys/`, `HASHES.txt`). Gap recall, action recall and every scored figure keep their
  values; the new sections are additions.
- **Byte-identical regeneration** holds for everything generated (`eval`, `gaps`, `replay-page`, `site`, the new
  datasheet and intent file): CI's `git diff --exit-code` stays.
- **Report stays 5 pages.** Part D rebuilds the docx once and counts pages with `scripts/report_pages.ps1`; cut rule in
  Part D.
- Fault injection is labelled as such on every page it appears on: "the model call is made to fail at this step;
  nothing else changes".
- No entry name (another team, another team, another team, another team) appears in any tracked file (existing test).

## Review focus (what a judge attacks first)

1. "The model died; who decided?" The page shows a `model_unavailable` event, then a gate verdict with a clause, then
   the named human, and says no model was involved in that step. Part A.
2. "Your gap recall is one number; which gaps did you miss?" The table names them, scenario by scenario. Part B.
3. "Is that clause binding?" Every cite on every replay page says binding, advisory or method, and UAE or foreign. Part C.
4. "Is gap-12 the 'no agentic AI' gap?" The row maps to Y.3173 and Readiness first, then names the three unmeasured
   things. Part D.

---

## Part A: the model is down, the gate still decides

**Files:** `onyx/coordinator.py` (an except path), `onyx/model.py` (`FailingModel` wrapper), `onyx/modeldown.py`
(new), `docs/replay/model-down-S2.md` (new, generated), `onyx/replay_viewer.py` (one picker entry), `onyx/site.py`
(the what-if page gains a second section, or a sibling page; builder's choice, say which), `tests/test_modeldown.py`,
`README.md` (one paragraph under the what-if paragraph), `docs/report.md` (one sentence, Part D applies it).

**Produces:** `python -m onyx model-down <log> --at <step> [--out DIR]`: replays the log as `whatif.replay_under` does
(copy its setup; `runs.py` untouched), with the model wrapped so that the call at `--at` raises what
`OpenAICompatibleModel` raises after its last attempt. The coordinator's except path then:
1. appends a `model_unavailable` event (actor the step's agent, `new_value`: error class, attempts, elapsed, the step),
2. authors a plain-code proposal from the coordinator, verb `escalate_to_human`, target the named human the scenario's
   facts name for that step (or "a named trained human (licence 9.1)" when the facts name none), clause ids the
   complaint gate's (CPR 26.7.2, licence 9.1) when the step is a complaint step, else none, quote from the chunk,
   `reason: "model unavailable"`,
3. submits it to the gate as a pending proposal (addendum 29 shape), so deny-by-default or the complaint gate decides,
4. continues the run (later steps call the model as before; in replay they come from the log).

The page: title, the run, chain ok, the fault injection sentence, then a two-column table recorded against model-down
for every decision of the step and the steps after it, then "What stays" (count identical), then one line: "No model
took part in step 3 of the model-down column." Same shape as `whatif-S2-gap-1.md`.

Live runs: the same except path runs when a real model dies (the retry loop in `model.py` is unchanged); the run no
longer crashes; the event and the hold are logged. Not exercised live in this task (USD 0); the test covers it with
`MockModel` raising.

- [ ] `test_failing_model_raises_at_step` (`FailingModel` raises only at the named step, delegates otherwise).
- [ ] `test_coordinator_survives_model_failure` (S1 scripted, `MockModel` raising at step 2: run completes; the log has a
  `model_unavailable` event, then a gate event with verdict `hold`, chain verifies).
- [ ] `test_model_down_s2_hands_over` (replay `runs/c5/S2/run1.jsonl` with `--at 3`: recorded verdict `block`; model-down
  verdict `hold` or `block` with `escalate_to_human` to the same human the recorded run names; every other decision
  identical; the page is byte-identical on rerun).
- [ ] `test_c5_logs_replay_unchanged` already exists; it must still pass (run it, quote the count).
- [ ] Viewer: a picker entry "Model down: S2, the call at step 3 fails" that renders the page's text, beside the what-if entry.
- [ ] Site: the entry reachable from `index.html` and `runs.html` in one click; CI diff stays empty.
- [ ] README: one paragraph after the what-if paragraph: what it shows, the command, the page link, the label sentence.
- [ ] Commit `feat: model-down fault injection on the recorded S2 run (USD 0)`; PR; CI green; report-back
  `docs/report-back/2026-10-3x-task-29a-model-down.md` with the page pasted.

**Stop and ask when:** the coordinator cannot author a proposal without a model call for the complaint step (then
describe what it needs); the gate returns `allow` for the authored proposal (that would be wrong; do not change the gate);
any committed log changes.

## Part B: eval, three sections, no figure moves

**Files:** `onyx/eval.py`, `eval/results.md` and `.json` (regenerated), `README.md` (results block), `tests/test_eval.py`.

**B1, expected / found / missed / unexpected gaps.** New section "Gaps against the keys (C5)" in `results.md`, one row
per scenario and language, over both runs: expected ids (from the key); found in every run; found in some runs (name
the run count); missed; unexpected (ids flagged that the key does not name: register rows and candidates, listed by id,
with a count of flags that name no register id). Plus one summary line, numbers from the logs: "N of M expected gaps
found in every run; K missed (list); U unexpected register ids flagged". Gap recall itself does not change. The
summary line is exported in `results.json` under `c5.gaps_vs_keys` so the report build can check it (Part D).

**B2, intervals.** For action recall (pooled over 112 steps; per language over 56) and citation validity (over the
cited proposals, count stated), a 95% Wilson interval beside the point figure in the C5 summary table and in
`results.json` (`ci95: [lo, hi]`, `n`). One caveat line in the metric definitions: "the interval treats key steps as
independent trials; they are not (steps of one run share a conversation), so read it as a rough width, not a
guarantee". The README results block shows the pooled action-recall interval only.

**B3, citation failures by kind.** Shown only, never compared: for C5, each invalid citation with its run, step, cited
id and kind in {id unknown, id in another document, quote not verbatim, chunk not VERIFIED}; a count per kind. One
definition line: validity here means the quote is verbatim in the cited VERIFIED chunk the agent was given; a citation
that fails never reaches an action (the gate rejects it before the act).

- [ ] `test_wilson_known_values` (two hand-checked cases, e.g. 110 of 112 and 54 of 56, to three decimals).
- [ ] `test_gaps_vs_keys_s1_misses_two` (S1 C5: expected three, found one in every run; the two missed named).
- [ ] `test_eval_is_idempotent` passes; `eval/results.md` diff shows only added sections and the CI figure columns.
- [ ] Scored figures unchanged: quote the six C5 means before and after in the report-back.
- [ ] Commit `eval: gaps against keys, Wilson intervals, citation failures by kind`; PR; CI green; report-back.

**Stop and ask when:** any scored mean changes by any amount; the unexpected-gap count is zero in every run (then
show the flag events, something is off in the match); an interval needs a library.

## Part C: pages and the KB

**Files:** `onyx/replay_page.py`, `onyx/replay_viewer.py`, `onyx/html_kit.py`, `docs/replay/*` (regenerated),
`docs/site/*` (regenerated), `onyx/kb.py` (`datasheet`), `kb/DATASHEET.md` (new, generated), `docs/intent.json` (new,
generated by `python -m onyx intent`), `README.md`, tests.

**C1, binding label on every cite.** Every clause cite on the replay markdown pages, the viewer and the site's runs
page gains `binding` / `advisory` / `method` and `UAE` / `foreign` / `international` from `rules.json` (fall back to
the manifest's `binding_status` and `jurisdiction` for a cited chunk with no rule row), rendered as a short tag after
the page number. Design-basis reasons (IMDA, EU AI Act, GDPR) keep their `design_basis` kind and show `method` or
`foreign`, never `binding`.

**C2, datasheet.** `python -m onyx kb datasheet` writes `kb/DATASHEET.md` from the manifest and `kb/chunks/`: what is
in (counts by status, binding_status, jurisdiction, language, pairs EN/AR), which language prevails per instrument
(manifest `notes`), how documents were fetched and verified (sha256, `kb verify`), why sources are not redistributed
(addendum 15), what is committed (144 cited clauses, 18 documents), the ITU set reviewed and what was kept (one line;
if the README does not say it, write it from the manifest), known limits (the 16 landing URLs with `LANDING_MARK`,
the 3 UNVERIFIED rows backing no claim, the lam-alef trap, Telecom Law Arabic read from page images, Art 14(3) quoted
from the Arabic), licence notes, and the generation line. Byte-identical; CI runs it and diffs. README first screen
links it beside the `Inputs.md` link. `docs/site/kb.html` links it.

**C3, ML Intent (optional, last; skip if Parts A to C1 overrun 11-02).** `python -m onyx intent` writes
`docs/intent.json`: manifest ids by node, agents with verbs and document sets, model id as C5 recorded it, prompt
version, gate version, key hashes, the four verdicts, the scenario ids. Named in the README's MLFO row as "ML Intent:
`docs/intent.json`". Nothing reads it at run time; say so in its first key (`"note"`).

- [ ] `test_every_cite_carries_binding_tag` over every regenerated replay page; `test_design_basis_never_binding`.
- [ ] `test_datasheet_counts_match_kb_verify` (the counts in `kb/DATASHEET.md` equal `kb verify`'s output).
- [ ] `test_datasheet_idempotent`, `test_intent_idempotent`.
- [ ] Pages: `tests/test_pages_grounding_readme.py`, `tests/test_replay_viewer.py`, `tests/test_site.py` updated for the
  tags; screenshots in `docs/replay/screenshots/` and `docs/site/screenshots/` re-taken (headless Chrome) only where a
  tag is visible in the framed step.
- [ ] Commit per sub-part; PR; CI green; report-back.

**Stop and ask when:** a cited chunk has neither a rule row nor a manifest row (name it); the datasheet needs a fact
that is not in the manifest or the README (do not write it from memory).

## Part D: words, then one report rebuild

**Files:** `onyx/data/gaps.json` (gap-12), `docs/gaps.md` and the README register (regenerated), `docs/report.md`,
`docs/report.docx` (rebuilt once), `docs/build_report.py` (new checks), `tests/test_report.py`.

**D1, gap-12.** The row's `gap` text and the report's gap-12 line open with the mapping, then the absence. Report line,
replacing the current gap-12 row text, same cell, about the same length:

"Agent authority: Mizan's stop at S2-3 sits at Y.3173 'Human and System' on the decision step (Table 7-1) and its
hand-over is Readiness D9's inference-to-action latency in the other direction; mapped there, neither text measures
when an acting agent must stop, how often it hands over or how long that takes (Table 7-2 NOTE 1 gives a human's order
the highest authority; it never requires the system to ask)."

`gaps.json`: the `gap` field gets the same two-part shape in full (quotes and pages from the 10-26 ruling, sections 2
to 4, already in the row's `searched` list); `recommendation` unchanged. The site and `docs/gaps.md` regenerate.

**D2, report sentences** (from Parts A and B; `build_report.py` checks each number against `eval/results.md`):
- S2 paragraph, after the what-if sentence: "With the model call made to fail at step 3, the coordinator's deny-by-default
  hold hands the conversation to the same human, with no model in that step (`docs/replay/model-down-S2.md`)."
- Results paragraph: replace "gap recall 0.87" with the B1 summary line in its shortest form: "expected gaps: N of M
  found in every run, K missed (both in S1), U unexpected register ids flagged"; and after "0.96 / 1.00 (110 of 112 key
  steps ...)" add "95% interval 0.94 to 1.00 pooled" with the numbers B2 produced, never typed.
- Introduction, the link list is the submission-day order's job; nothing here.

**D3, the cut rule.** Rebuild the docx; count pages with `scripts/report_pages.ps1` (PowerShell tool). If Word says 6,
cut in this order, one at a time, recount after each: (1) Results: "(one cited id in the English S2 runs lacked its
language ending)" becomes "(one id, S2 English)"; (2) Limits: "ITU can reuse the Arabic clause chunks and runs (SNAI),
the verified manifest and the five agent manifests." becomes "ITU can reuse the Arabic chunks and runs, the manifest
and the agent manifests (SNAI)."; (3) S3: "A de-identified payload under the processor contract: allow, what left
logged." becomes "A de-identified payload under the processor contract: allow." If still 6 after cut 3, stop and ask
with the page and word count.

- [ ] `test_report_gap12_maps_before_claiming` (the gap-12 cell contains "Y.3173" and "D9" before "neither").
- [ ] `test_report_figures_match_eval` extended to the B1 line and the interval.
- [ ] Count check: every number the report states, listed with its source line in `eval/results.md`, in the report-back
  (not only the ones this task touched).
- [ ] `hq` copy: `docs/report.md` copied over `D:\Projects\hq\uni\ai-for-good-hackathon\report-draft-2026-10-23.md`
  (keep the `.bak-2026-10-28`; add `.bak-2026-10-3x`).
- [ ] Commit `report: gap-12 mapped first; model-down and gaps-against-keys sentences; 5 pages`; PR; CI green;
  report-back with the page count output pasted.

## Timeline

| Date | Work |
|---|---|
| 2026-10-30 | Part A (6 h) |
| 2026-10-31 | Part B (3 h), after session 5 and the sweep read; if ITU's design comment or session 5 changes anything, hq re-rules before Part C |
| 2026-11-01 (class day) | Part C1, C2 (4 h) |
| 2026-11-02 | Part C3 if time, Part D (3 h), merge to main, CI green, tag `task-29` |
| 2026-11-03 | buffer; video script starts (video-hq) |

## Done means

All four PRs merged; CI green on main; `eval/results.md` carries the three new sections with the six C5 means
unchanged; `docs/replay/model-down-S2.md` exists and the viewer and site show it; every cite on every replay page
carries a binding tag; `kb/DATASHEET.md` exists and matches `kb verify`; the report's gap-12 row maps first; Word says
5 pages; no file under `runs/` or `onyx/data/keys/` changed (`git diff --stat df7c29c -- runs onyx/data/keys` empty);
recorded spend still USD 21.85.

## Not in this order

Anything in the ruling's section 4 (live app, re-record, unseen runs, masking, self-reconfiguration); the video;
the submission-day list (link list, members line, Pages source, README claim table, reviewer line); the judge card
lines (hq writes them from the ruling's section 3 "Shows" column when the video script is written).
