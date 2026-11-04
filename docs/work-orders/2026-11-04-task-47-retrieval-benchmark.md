# Task 47: retrieval measured on its own, English and Arabic, current embedder and a bilingual one (order written on Fable, 2026-11-04)

Decided in `D:\Projects\hq\uni\ai-for-good-hackathon\rival-strengths-read-2026-11-04-fable.md`, section 10. Build on
Opus, after Task 45 is merged, before 2026-11-06; it ranks above Task 46 if only one fits. Start with `git pull` on
main. Branch `task-47`.

## Why

Criterion 1 is scored on "completeness, accuracy, and structure of ingested national material; ability to retrieve
relevant policy context under query" (rules checklist section 4). Mizan prints no retrieval figure of its own: the
"Key clauses shown" table (`eval/results.md` line 172) says 26 of 234 key clauses in English and 6 of 234 in Arabic
reached the model by retrieval alone; the rest came by the mandate list. Annex A says the embedder is English-centred
and a bilingual one is "the obvious upgrade" (lines 20 to 25). A judge reading criterion 1 can ask "how well does your
retrieval work?" and today the honest answer is a design argument and two low numbers. This task gives the number,
for both languages, for the embedder we ship and for a bilingual one, with no model call and no change to any
scored run.

## Task

1. **A retrieval-only benchmark, no model.** For every key step with a `must_cite` list (`onyx/data/keys/S1..S5.json`;
   S1-1 and S2-1 have no model call and are included here because retrieval runs on the step text, not the model),
   query the retriever with the step's input text as the agent receives it (the scenario file's text for that step,
   `onyx/data/scenarios/S*.json`, English and Arabic), without the mandate list, and record whether each `must_cite`
   chunk is in the top 8. Report recall@8 per scenario and language and pooled, with the Wilson interval the other
   rows use, and recall@1 pooled. Same chunk mapping as "Key clauses shown" (`eval.py`: each must_cite entry maps to
   its chunk; two rules on one chunk count twice).
2. **The same benchmark with a bilingual embedder, shown, never compared with C5.** Embed the same `kb/chunks/` with
   a multilingual sentence-transformers model into a separate index under `kb/index-bilingual/` (git-ignored, with a
   build command and the model name and revision in the results), run the identical queries, print the same rows
   beside the first. Model order to try: `intfloat/multilingual-e5-base`, then `-small`, then `BAAI/bge-m3`; the
   first that loads and embeds the whole corpus in under 30 minutes on this machine is the one; name it. The shipped
   pipeline keeps `all-MiniLM-L6-v2`; nothing in `onyx/model.py`, `onyx/agents/`, `onyx/gate.py`, `rules.json`,
   the mandates or any run changes.
3. **One new section in `eval/results.md`**, "Retrieval alone (no model, no mandate list)", two tables (shipped
   embedder; bilingual embedder, labelled "not used in any scored run"), the method lines in the same style as the
   existing method list (lines 349 to 360), and the sentence that ties them to "Key clauses shown": the scored runs do
   not depend on retrieval alone because the mandate list comes first.
4. **Annex A, Retrieval paragraph (`docs/annex.md` lines 20 to 25 and 61 to 68): two sentences at most**, pasting the
   printed figures: recall@8 English and Arabic with the shipped embedder, and with the bilingual one, "measured on the
   key steps, no model call; the bilingual embedder is not in any scored run". Rebuild the report PDF; the page count
   of the report body and the annex must be unchanged (state both in the report-back). If the annex grows a page, cut
   the two sentences to one.
5. **README, "Three things to look at first" or the reviewer table's Knowledge base row: one clause** naming the
   retrieval figure and the results section. No other README text changes.
6. **Tests:** `tests/test_eval.py` gains the benchmark's unit checks (chunk mapping equals "Key clauses shown";
   recall arithmetic on a fixed fixture; the bilingual table is absent, not wrong, when the index is missing). The
   bilingual index is not built in CI; `eval` prints "bilingual index not built" and skips that table.

## Done means

1. `uv run python -m onyx eval` prints both tables locally; the report-back pastes them.
2. `uv run pytest` green locally; CI "reproduce" green on the PR (without the bilingual index).
3. `docs/report.pdf` rebuilt; body and annex page counts unchanged and stated.
4. Every number in the annex sentences equals a printed value in `eval/results.md` (the report-back lists each pair).
5. Report-back in `docs/report-back/` with the model name and revision, index build time, and the two tables.

## Limits

- No model call, no new recorded run, no prompt, gate, key, mandate or rules change. `onyx/data/keys/`, HASHES and
  `runs/` are never edited. API spend: zero.
- The seven layers of `_reference/llm-agents.md`: none touched; nothing shipped or deferred changes.
- No competitor is named anywhere.
- The figures are printed as found. If Arabic recall@8 with the shipped embedder is low, it is printed low; the
  annex already says the design does not depend on it. Do not soften the number.
- Stop and ask if: the step input text for a key step is not recoverable from the scenario file (then name the step
  and stop); the bilingual embedder cannot load within 15 minutes of trying the three names (then ship part 1 alone,
  the shipped embedder's table, and say so in the annex sentence); the annex gains a page after the one-sentence cut.
