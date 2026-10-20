# Work order: Onyx, ITU AI for Good Lab Hackathon UAE 2026, telecom T1

Written 2026-10-17 on Fable. Build runs on Opus in a new folder inside the engineering root,
`D:\Projects\engineering\onyx-hackathon-build` (corrected 2026-10-17; rename before the repo goes public if wanted). Submission 2026-11-09.

> **For agentic workers:** use superpowers:executing-plans (native) or subagent-driven-development to run
> this task by task. Steps use `- [ ]` boxes.

**Goal:** a public repo plus a 5-page report and a 7-minute video showing a UAE operator's consumer-care AI
whose every action passes plain-code gates written from binding UAE text, run governed and ungoverned, with
a hash-chained log, replayable runs, frozen answer keys, and a gap register the public competitor does not have.

**Architecture:** five agents (care, policy and legal adviser, TDRA, Data Office, coordinator) over one
knowledge base. The model proposes JSON actions; `gate.py` (the Y.3172 P node) decides in plain code from
KB clauses; the coordinator releases scenario events in stages to different agents; every step is appended
to a hash-chained JSONL log; `eval` recomputes every report number from the logs.

**Tech stack:** Python 3.12, `uv`, ChromaDB (three collections, reference-code layout), `pytest`, one
OpenAI-compatible model adapter with a recorded-response mode (runs replay without an API key), a Rich CLI.
No GUI (Saudi S2 00:41:12: a CLI beats a GUI).

## Only these sources

Every rule, figure and name in the build traces to one of these. Nothing from memory.

| Source | File (under `D:\Projects\hq\uni\ai-for-good-hackathon\`) |
|---|---|
| Hackathon rules, scoring, report sections, Y.3172 nodes, Readiness names | `rules-checklist-2026-10-14.md` sections 3, 4, 5, 6, 10, 11 |
| Organisers' gap method, what wins | `mentoring/saudi-sessions-notes-2026-10-17.md` |
| The plan as of 2026-10-15 (agents, gates, scenarios) | `hackathon-plan-2026-10-15.docx` (text in `plan-2026-10-13.md` and the background) |
| CPR v2.0 clause table, Arabic check, gap verdicts, build changes | `cpr-full-read-2026-10-15.md` |
| Telecom Law, 2026 licences, PDPL, Electronic Transactions, Consumer Law, Cabinet 56/2024, Spam Calls v4, Child Digital Safety: gap verdicts and build changes | `telecom-law-and-licences-2026-10-17.md` sections 5, 6, 7 |
| Perplexity verdict and the seven stage-2 changes | `perplexity-2026-10-17/verdict-2026-10-17.md` |
| Competitor and DoH reading notes | `standards-text/doh-abu-dhabi-2026-10-17/reading-notes-2026-10-17.md` and `competitor-another team-README.md` |
| ITU reference code KB layout | `research-itu-reference-code-2026-10-14.md` |
| Saudi winners' proof pattern and judge card | `saudi-winners/another team_README.md`, `saudi-winners/another team_JUDGE-QA.md` |
| Global examples, read 2026-10-17 on Fable | `standards-text/global-2026-10-17/imda-agentic-ai-v1.5.txt`, `eu-ai-act-art50-art113-20260727.txt`, `gdpr-art22.txt` |
| Primary texts | `standards-text/` (CPR EN and AR, DoH, competitor) and `corpus-text/` |
| Opening figure (item 25): e& UAE complaints 2023 to 2025, TDRA complaints 2020 to 2023, TDRA telemarketing complaints 2025, Etisalat's Virtual Assistant page, TDRA release 2024-04-02 | `perplexity-2026-10-20/opening-figure-read-2026-10-20.md`; PDFs and text in `standards-text/eand-sustainability-report-appendices-2025.*` and `standards-text/tdra-sustainability-report-2023-*` |

## Global constraints

- Decisions are plain code, never model scores (2026-10-14). The model proposes and explains; it decides nothing.
- Every mandate verb, threshold and clock in the gate cites a KB row; `check-data` proves each quote is verbatim.
- KB rows carry `status` (text provenance) in {VERIFIED, REFERENCED, UNVERIFIED, HISTORICAL}, `binding_status` in {binding, advisory, method} and `jurisdiction` in {UAE, foreign, international}. A `block` cites only rows that are VERIFIED, binding and UAE; everything else is design basis in the reasons (verdict change 2; replaced 2026-10-20, addendum item 13).
- Y.3172 node names: SRC, C, PP, M, P, D, SINK, plus MLFO and ML sandbox, per clause 8.1, not the reference repo's summary.
- Readiness dimensions by their official names from checklist section 11 only.
- 26.7.2 is a binding rule the system enforces, never listed as a gap (verdict change 4).
- The CPR is quoted in both languages where the Arabic differs (17.2 "calendar days"; 26.7.2 "يستثنى أو يستبعد منها").
- The five CPR annexes are not published; the dispute procedure cites the TDRA service page (5, 10 or 15 working days).
- Operator, subscribers and numbers are synthetic and labelled so on every screen and in the README. Law texts are real, public, linked, hashed.
- Report: max 5 pages, template order (checklist section 6), English; KB as an appendix; video max 7 minutes with subtitles, submitted with the first round (2026-10-14 decision).
- No consumer data, no confidential documents (Saudi S3 00:30:32: a team was banned).
- Unsourced claims stay out of the report: that UAE operators run AI care agents today, that subscribers suffer the four harms, the "AI-readiness" licence claim (dead, 2026-10-17).
- Repo licence MIT for code; KB documents stay their publishers'.
- Model API keys in `.env`, never committed; every scored run is committed with its recorded responses.

## Review focus (what a judge attacks first; each has a test in the owning task)

1. "Show it running now, not slides" (another team Q1): `python -m onyx run S2 --replay` must work offline in under a minute. Task 10.
2. "Is 26.7.2 really a bar on chatbots in complaints?" The hand-over event quotes both languages and licence 9.1. Task 6.
3. "That gap is not a gap; there must be a document" (S2 25:23): every gap row names the clauses searched and what they say. Task 9.
4. A judge adds a step with no rule in the KB: the agent returns `INSUFFICIENT_EVIDENCE` and the gap register gets a candidate row, live. Task 7.
5. "Your numbers are yours": answer keys hashed before the first live run, `eval` regenerates every figure, CI badge reruns it. Tasks 8 and 11.

---

## Task 1: Folder, repo, scaffold

**Files:** in `D:\Projects\engineering\onyx-hackathon-build\` (path corrected 2026-10-20; the folder exists and holds this order), create `pyproject.toml`, `onyx/__init__.py`, `onyx/__main__.py`,
`tests/test_smoke.py`, `README.md` (synthetic-data notice at the top), `LICENSE` (MIT), `.gitignore` (`.env`, `data/chromadb/`),
`.github/workflows/reproduce.yml` (placeholder that runs `pytest`).

**Produces:** CLI entry `python -m onyx <command>`; commands added by later tasks: `kb`, `run`, `replay`, `verify-log`, `eval`, `check-data`, `selftest`.

- [ ] Run `D:\Projects\engineering\_reference\new-repo.md` first (git, private remote on SHRA1M, order filed in `docs/work-orders/`, CLAUDE.md, brief, plan approved). Its `.gitignore` list is added to the one above. Then `uv venv`, `uv pip install -e '.[dev]'`.
- [ ] `tests/test_smoke.py::test_cli_help` asserts `python -m onyx --help` exits 0. Run, see it fail, implement, see it pass.
- [ ] Add the folder to `D:\Projects\engineering\engineering-map.md` (thinking folder: `hq\uni`) and to `D:\Projects\hq\hq-map.md` under "Code lives in engineering" (private until 2026-11-09, then public; notes stay in `uni/ai-for-good-hackathon/`).
- [ ] Commit `chore: scaffold onyx`.

## Task 2: Knowledge base manifest and ingestion

**Files:** `kb/manifest.csv`, `kb/manifest.schema.json`, `kb/sources/` (fetched texts), `kb/chunks/` (clause chunks as JSONL),
`onyx/kb.py`, `tests/test_kb.py`.

**Manifest columns (reference layout plus ours, 2026-10-14):** `document_id, title, issuer, instrument, url, sha256, fetched_at,
status, binding_status, jurisdiction_level, language, source_type, country, node`.

**Chunk fields:** `document_id, article, clause, page, text_en, text_ar, status, retention_class, node`.

**Rows, first pass (all from the sources table above; status VERIFIED only where the text is on disk in `standards-text/` or `corpus-text/`):**
TDRA CPR v2.0 EN and AR; Telecommunications Law 3/2003; the 2026 licence text in `telecom-law-and-licences-2026-10-17.md` section 3;
PDPL 45/2021; Electronic Transactions 46/2021; Consumer Protection Law 15/2020 and Cabinet 66/2023; Cabinet 56/2024 and 57/2024;
Spam Calls v4, Spam SMS; TDRA QoS v3.0; Child Digital Safety law; Decision 16/2026; Instructions 1/2014; the TDRA dispute service page;
Y.3172; Readiness Report 2.0 and `dimensions.json`; IMDA MGF Agentic AI V1.5; EU AI Act consolidated 2026-07-27 (Art 50, 113);
GDPR Art 22. The non-binding Ethics guideline 3.3.2.2 and the Deepfake Guide enter as SECONDARY. Cabinet agentic framework
(2026-05-18), Executive Order 3/2004, PDPL Executive Regulations enter as UNVERIFIED rows with `text` empty: their absence is evidence.

- [ ] `test_manifest_validates` (every row passes the schema; `sha256` matches the file on disk for VERIFIED rows).
- [ ] `test_chunk_cpr_26_7_2_both_languages` asserts the chunk for CPR 26.7.2 holds the English "preclude the use of non-human agents" and the Arabic "يستثنى أو يستبعد منها".
- [ ] Implement `kb.fetch()`, `kb.verify()`, `kb.ingest()` (ChromaDB `kb_main`, `kb_framework`, `kb_decisions`, cosine; chunk by clause, not by word count, so a citation is a clause id).
- [ ] `python -m onyx kb export` writes the ITU InputDocs layout (`Inputs.md` manifest style).
- [ ] Commit.

## Task 3: Mandates, rule table, answer keys (frozen before any live run)

**Files:** `onyx/data/mandates.json`, `onyx/data/rules.json`, `onyx/data/scenarios/S1..S5.json`, `onyx/data/keys/S1..S5.json`, `tests/test_data.py`.

**mandates.json:** one entry per agent with the verbs it may use and the clause each verb hangs on. Care agent: `propose_sale`, `propose_change`,
`disclose_account`, `draft_reply`. Policy adviser: `classify_channel` (CPR 4.15/4.17/4.22/4.23), `cite`, `flag_gap`. TDRA: `raise_dispute`
(26.16.1, 3 business days), `order_restore`, `request_report`. Data Office: `receive_objection` (PDPL 18(1)), `receive_dpia` (21(2)(a)),
`request_human_review` (18(4)). Coordinator: `release_event`, `route`, `escalate_to_human`.

**rules.json, every row with `clause`, `verb`, `value`, `unit`, `language_note`:** CPR 4.3, 4.4 (three renewal conditions), 4.6, 4.7.1 to 4.7.3,
4.10, 4.11, 4.17.3, 4.22.1 to 4.22.3, 4.23.3, 5.4.1, 9.4.2, 13.6, 16.9.2, 17.2 (28 calendar days), 22.1.1, 22.1.2, 22.2, 22.3, 22.4, 22.5,
24.5, 24.6 and fn 35, 24.7, 24.9, 24.10, 26.6, 26.7.1, 26.7.2, 26.13.2, 26.13.3 (immediately / one business day), 26.14.2 (20 business days),
26.16.1, 3.2.2, 3.3, 3.9 (retention classes), 28.11, 28.25, 28.26; licence 9.1, 9.2.4, 9.4.3, 3.4.1; PDPL 6(1)(b), 7(5), 8(1), 13(2)(d), (g),
17, 18(1), 18(2), 18(4), 21(2)(a), 22, 23(1)(a); Electronic Transactions 10, 11(2), 12(2)(b), 28(1), 33; Consumer Law 4(5), 8(4), 29;
Cabinet 66/2023 Art 34(1), (3), (5); Cabinet 56/2024 Art 4, 5(6), 5(7); Spam Calls v4 3.3(iii), 9.5, 10.2, 14.3, 15.4; Child Digital
Safety 7(1), 11(1)(b); Decision 16/2026 4.17 to 4.19 (two hours); QoS v3.0 T1(2a); Cybercrimes 48. Exact wording from the clause tables in
`cpr-full-read-2026-10-15.md` section 2 and `telecom-law-and-licences-2026-10-17.md` sections 2 to 4.

**Answer keys:** per scenario, the expected gate verdict per step, the clauses that must be cited, the gap(s) that must be flagged, and the
one step whose correct answer is `INSUFFICIENT_EVIDENCE`. Written by Iyas and the assistant, then `sha256` of each key file recorded in
`onyx/data/keys/HASHES.txt` and committed before Task 8's first live run. The commit hash is quoted in the report.

- [ ] `test_every_rule_quote_is_verbatim`: each `rules.json` row's `quote` appears verbatim in the KB chunk it cites (this is `check-data`).
- [ ] `test_every_mandate_verb_cites_a_clause`.
- [ ] `test_keys_hashed`: `HASHES.txt` matches the key files.
- [ ] Commit `data: mandates, rules, frozen answer keys`.

## Task 4: Audit log, hash chain, replay store

**Files:** `onyx/audit.py`, `tests/test_audit.py`.

**Event schema (reference AuditLog fields plus ours):** `seq, ts, prev_hash, hash, actor, action, entity_type, entity_id, old_value, new_value,
source, reason, clause_ids[], quote, verdict, model_request_id, model_response (recorded verbatim)`. `hash = sha256(prev_hash + canonical_json(event))`.

**Produces:** `append(event) -> hash`, `verify(path) -> bool`, `iter_model_responses(path)` for replay.

- [ ] `test_chain_breaks_on_edit`: change one byte in a committed line, `verify` returns False and names the line.
- [ ] `test_first_event_carries_key_hashes`: `run_start` holds the sha256 of every answer key.
- [ ] Implement; `python -m onyx verify-log <file>` prints `chain ok` or the first broken seq.
- [ ] Commit.

## Task 5: Model adapter and agents

**Files:** `onyx/model.py` (OpenAI-compatible client; `RecordedModel` that replays responses from a log; `MockModel` for selftest),
`onyx/agents/{care,adviser,tdra,data_office,coordinator}.py`, `onyx/agents/base.py`, `tests/test_agents.py`.

**Agent output schema (from the reference code, kept):** `agent_name, proposals[{verb, target, args, clause_ids[], quote, rationale}],
sources_used[], reasoning_chain[]`. Agents retrieve only within their mandate's document set (mandate-scoped retrieval).
Agents talk to each other through typed JSON, never free text (IMDA 2.3.1: structured schemas between agents).

**Model choice:** left open for Iyas: any OpenAI-compatible endpoint works. Record the model id in every run. Decide by 2026-10-20.

- [ ] `test_care_agent_cannot_call_order_restore` (verb outside mandate is rejected before the gate).
- [ ] `test_adviser_classifies_channel`: voice -> 4.17, app chat -> 4.22 plus 4.10, web -> 4.23, and the classification is logged.
- [ ] `test_mock_model_runs_offline`.
- [ ] Commit.

## Task 6: The gate (P node)

**Files:** `onyx/gate.py`, `tests/test_gate.py`. Pure functions, no model calls.

**`decide(proposal, state, kb) -> Verdict{allow|hold|block|insufficient_evidence, clause_ids, reasons[]}`.** A proposal passes only if:
quote of 20+ characters is verbatim in a chunk the proposing agent retrieved; chunk status VERIFIED; verb in the agent's mandate; the
inject it answers was released to that agent; any deadline comes from `rules.json`.

**Gates, each a function with the clauses it enforces (from the 2026-10-15 plan, the CPR read section 4, and the 2026-10-17 section 7):**
- `consent_gate`: 4.3, 4.6, 4.7.1 to 4.7.3, 4.10 plus 4.11 OTP (strict reading), 5.4.1, 3.9 five years, 4.4 three renewal conditions tested not the label, 4.22.3 "no" default, 9.4.2 partner cap, 16.9.2.
- `disclosure_before_sale_gate`: the agent states it is automated before any purchase step and logs it; Electronic Transactions 11(2) (validity of the sale), EU AI Act 50(1), 50(5) as the global example.
- `sharing_gate`: 24.6 and fn 35 (recorded consent, contractual or later, no opt-out exercised), 24.7, 24.9, PDPL 7(5); `model_provider_gate`: minimum de-identified payload, processor contract on file (8(1)), foreign-recipient notice (13(2)(d), (g)), log what left, cite 72(2).
- `verification_gate`: classify the request by Electronic Transactions Art 33 trust level; refuse account data below the level the adviser set; log the level (24.10).
- `disconnection_gate`: 22.1.1 notice and 22.2 content first, 22.1.2 confinement, 22.3, 22.4, 22.5 exception, DPIA on file (21(2)(a)), human review on request (18(4)), no reliance on a unilateral-termination term (66/2023 34(3)); GDPR 22(3) as the global example.
- `complaint_gate`: on 2.1.7 trigger the AI stops, issues reference and time-frame (26.13.2, immediately), hands over to a human (26.7.2 in both languages, licence 9.1), logs the IVR-equivalent moment for QoS T1(2a); the AI may `draft_reply` for the human only.
- `price_gate`: quoted figures from the KB only; 3.3, 5.3, Consumer Law 29, Cybercrimes 48. `price_change_gate`: 17.2, 28 calendar days (English), opt-out route.
- `cancellation_gate`: 13.4, 13.6 immediate suspension, 13.8 no retention pitch before cancellation.
- `child_gate`: age or caregiver flag before any change or disclosure (Child law 7(1), 11(1)(b)); absent flag = unverified.
- `marketing_gate`: 56/2024 Art 4, 5(6), 5(7); Spam Calls v4 9.5, 10.2, 14.3, 15.4 (09:00 to 18:00); 28.25, 28.26; PDPL 17.
- `records`: complaints three years (licence 9.2.4), billing two (9.4.3), consent and 2FA five (CPR 3.9); Arabic copy of every contract or notice record (Consumer Law 8(4)).
- `deny_by_default`: any verb with no gate, or a human approver unreachable, returns `hold` (IMDA 2.2.2: deny action when approval infrastructure fails).

Ungoverned mode: `gate.decide` is replaced by `allow_all`, nothing else changes, so the diff is the gate alone.

- [ ] One test per gate, governed and ungoverned, using the scenario step that exercises it; `test_complaint_gate_quotes_both_languages`; `test_unknown_verb_is_held`; `test_unverified_source_never_allows`.
- [ ] Implement; commit `feat: gate`.

## Task 7: Scenarios and the coordinator (staged release, live step)

**Files:** `onyx/coordinator.py`, `onyx/data/scenarios/*.json`, `tests/test_scenarios.py`.

**Scenarios (plan 2026-10-15, plus 2026-10-17 additions), each with numbered steps, which agent receives each step, and one step whose
right answer is `INSUFFICIENT_EVIDENCE`:**
- S1 Roaming before a flight: single "yes" to a bundle; governed: disclosure, OTP, PSCM, consent record; unanswerable step: is the bundle a 4.4 "renewal"?
- S2 A billing question becomes a complaint: hand-over; unanswerable step: how fast must an app chatbot hand over (gap 2).
- S3 A partner wants the data for co-marketing, and the model provider is abroad: sharing and model-provider gates; unanswerable: adequacy of the destination (PDPL 22, no list).
- S4 Non-payment: warning, confinement, emergency numbers, human review on request; unanswerable: deadline for the 18(4) review (none exists).
- S5 TDRA dispute and a loss report: 26.16.1 three business days, Decision 16/2026 two-hour block after identity verification; unanswerable: what "adequate verification" is (24.10).
- Unseen bank (not in the repo's demo set, kept in `onyx/data/scenarios/unseen/` for the drill): price rise without notice; advert aimed at a child; charge for a fault repair; voice data request without verification; retention pitch delaying a cancellation; a security-authority disconnection request (22.5); an upgrade under 66/2023 34(5).
- Every scenario runs in English and Arabic (CPR 3.2.2); the Arabic run is scored too.

**Live step:** `python -m onyx run S2 --inject "<text>"` appends a step at run time; if no VERIFIED chunk answers it, the adviser returns `INSUFFICIENT_EVIDENCE` and `gaps/candidates.jsonl` gets a row.

- [ ] `test_staged_release`: at step 2 the TDRA agent has not seen step 1's subscriber data.
- [ ] `test_live_inject_with_no_rule_flags_gap`.
- [ ] `test_arabic_run_cites_same_clause_ids_as_english`.
- [ ] Commit.

## Task 8: Runs, replay, eval

**Files:** `onyx/eval.py`, `runs/S1..S5/run{1..3}.jsonl` (governed) and `runs/ungoverned/`, `eval/results.md`, `eval/results.json`, `tests/test_eval.py`.

**Metrics, each recomputed from the logs:** gate rejection rate; citation validity (quote verbatim and VERIFIED); action recall and obligation
recall against the frozen keys; gap recall; abstention (the unanswerable step answered `INSUFFICIENT_EVIDENCE`); hand-over latency in steps;
ungoverned baseline: claims the gate would have rejected; Arabic versus English agreement on clause ids. Three runs per scenario, min and max shown.

- [ ] `test_replay_matches_recorded_verdicts` on a committed run.
- [ ] `test_eval_is_idempotent`: running `eval` twice leaves `git diff` empty.
- [ ] Record three live runs per scenario per mode and commit them with responses.
- [ ] Commit `eval: results from runs/`.

## Task 9: Gap register and global examples

**Files:** `docs/gaps.md` (generated by `python -m onyx gaps` from `onyx/data/gaps.json`), `tests/test_gaps.py`.

**Row shape:** `id, gap, clauses searched (what they say), UAE position, global example (document, article, verified link, status), recommendation,
scenario step that exposes it, competitor has it (yes/no)`.

**Order (verdict change 4: lead with what the competitor lacks):**
1. When a conversation becomes a complaint and what the automated channel must do (CPR 2.1.7, 26.7.1 versus 26.7.2, licence 9.1, QoS T1(2a)).
2. Consent elicited by an AI: channel classification decides whether an OTP is needed (4.10, 4.17, 4.22, 4.23; PDPL 6(1)(b) "in writing or electronically").
3. "Adequate verification process" undefined for remote AI channels (24.10; Electronic Transactions 33 unmapped; Decision 16/2026 4.17).
4. Automated disconnection: no procedure, deadline or regulator for the 18(4) human review; 18(2) contract escape undercut by 66/2023 34 (quote both, inferred interaction). Global: GDPR 22(3).
5. Subscriber data to a hosted model provider: rule present, machinery absent (PDPL 22 list, 23(2), 8(11) never issued).
6. AI disclosure: no general duty; Electronic Transactions 11(2) makes it a validity condition for sales only. Global: EU AI Act 50(1), 50(5), in force 2026-08-02. Stated once, last, because the competitor claims it.
7. Five mentions of AI across every binding text, zero conduct standards (telecom section 5 item 3).
Candidates, flagged as such: child on the line (9), Arabic records (12), breach notification without a period (17), the Executive Order unpublished (11).

**Global examples, all read on Fable, cite by clause:** IMDA MGF Agentic AI V1.5 (2026-05-20, updated 2026-06-05): 2.1.2 deterministic limits
over prompt rules; agent identity (unique, accounted for, scoped, non-transferable); 2.2.2 checkpoints for high-stakes and irreversible actions,
override rate and response time as oversight audits, deny by default when approval infrastructure fails; 2.3.1 structured schemas between agents;
2.3.3 log immutability; 2.4.2 declare the agent upfront at the point of interaction, human contact points. EU AI Act Art 50(1) and 50(5)
(first interaction, accessible), Art 113 timing: general application 2026-08-02, Annex III high-risk 2027-12-02 after the 2026 amendment.
GDPR Art 22(1), 22(3) human intervention, point of view, contest.

- [ ] `test_every_gap_cites_searched_clauses_in_kb`; `test_every_global_example_is_verified_status`.
- [ ] Commit.

## Task 10: CLI demo, selftest, replay page (text)

**Files:** `onyx/cli.py`, `onyx/demo.py` (Rich tables: one strand per agent, accepted and rejected proposals, the gate's clause), `tests/test_cli.py`.

- [ ] `python -m onyx selftest` runs S1 with `MockModel`, no key, under 60 seconds, prints the headline figures from `eval/results.json`.
- [ ] `python -m onyx replay runs/S2/run1.jsonl` shows the hand-over step with both language quotes.
- [ ] `test_selftest_offline_under_60s`.
- [ ] Commit.

## Task 11: CI, README, KB export

**Files:** `.github/workflows/reproduce.yml`, `README.md`, `kb/README.md`.

CI on push: `selftest`, `pytest`, `verify-log` on every run, `replay` one run per scenario, `eval` then `git diff --exit-code`, `check-data`, `kb verify`.
README: badge, two-minute check block, scenario table, Y.3172 table (SRC scenario injects and KB sources; C per-agent inbox; PP clause chunking
and mandate-scoped retrieval; M the model; P `gate.py`; D coordinator routing, human hand-over, clocks; SINK audit log, gap register, demo;
MLFO engine and stage schedule; ML sandbox the governed-versus-ungoverned run), results block generated by `eval`, limits (answer keys are ours;
HITL scripted in recorded runs; UNVERIFIED rows cannot back a claim; no evidence UAE operators run such agents today).

- [ ] Push, badge green. Commit.

## Task 12: Report, video, judge card (stage 3 starts here, about 2026-11-02)

**Files:** `docs/report.md` and the docx on the ITU template (`report-template.docx`), `docs/JUDGE-QA.md` (another team shape, seven questions, EN answer, AR gloss, what to click), `docs/video-script.md`.

Report sections in template order (checklist section 6): title line with team Onyx, leader, members, contacts, GitHub link; introduction;
use case (problem, existing solutions and their problems, our solution, uniqueness: the gate diff, replay, frozen keys, Arabic, the five
gaps the competitor lacks); use-case requirements per node; mapping table (node, component, Readiness dimension, documents) claiming
depth on 6 Human Interface, 8 Collaboration with AI, 10 AI & Policies, 11 AI for Inclusion (Arabic, Instructions 1/2014 accessibility),
7 Strategy Alignment (operator, TDRA, Data Office); error scenarios as numbered steps including the controversial ones; policy and standards
gaps from the mapping. First paragraph and the video's first minute: the subscriber's harm (2026-10-14 headline). Last paragraph: the
TDRA test bench offer. Video: setup, each window, steps, expected and actual output, gaps and uniqueness, Iyas on camera, subtitles.

- [ ] Every number in the report is pasted from `eval/results.md` by a script (`docs/build_report.py`), never typed.
- [ ] Draft to the organisers for feedback (S4 00:42:42 offered it) by 2026-11-03.
- [ ] Final-day drills (2026-10-15 decision): judge card, 2 to 3 minute walk-through, cold unseen scenario, Arabic paraphrase, override shown and the path with no override (model-provider export).

## Timeline

| Dates | Work |
|---|---|
| 2026-10-18 to 10-20 | Tasks 1 to 3; Iyas picks the model API; answer keys frozen and committed |
| 2026-10-21 to 10-26 | Tasks 4 to 7 |
| 2026-10-27 to 11-01 | Tasks 8 to 11; first GPT round on the repo (cap two rounds) |
| 2026-11-02 to 11-06 | Task 12: report, video, judge card; organisers' feedback |
| 2026-11-07 to 11-08 | Fixes, final eval, tag `v1.0` |
| 2026-11-09 | Submit (deadline 2026-11-10, time and zone unknown; checklist 13.2) |

## Open before the build starts

1. Model API: Claude API key, Iyas pays per use until the 2026-11-18 shortlist brings ITU credits (decided 2026-10-20). Key not created yet: Task 1 walks him through it; the first live run waits for it, `MockModel` runs do not.
2. GPT review: dropped, and no GLM review either (Iyas, 2026-10-17). Claude builds and checks; OpenAI only for graphics polish at the end, if wanted.
3. Submission mechanism, deadline time zone, report file format: checklist section 13, still unanswered after session 3.
4. Team is four (2026-10-20): Iyas (leader), Mohammed Rawashdeh, Yanal Faouri, Zaid Saaydeh. Iyas builds alone; the team sheet (item 24) assigns the others' speaking parts once Iyas names them. Spellings from Iyas by voice, not yet seen in writing.

## Not read for this order

The competitor's code and KB manifest (README and report only); the DoH documents are out of scope now (health is the fallback);
the Readiness Report chapters for the five claimed dimensions (read them when the mapping table is written, Task 12);
the ITU reference code files listed as unread on 2026-10-14; the session 3 recording of 2026-10-17; anything in
`telecom-law-and-licences-2026-10-17.md` section 8.

## Addendum 2026-10-17 (Fable): changes from the Saudi reverse-engineering

Source: `saudi-judging-patterns-2026-10-17.md` section 6. These override the task text above where they differ.

1. Task 2: every KB record carries `status` in {VERIFIED, REFERENCED, METHOD}; `kb verify` prints the three counts; the README states them on its first screen.
2. Task 2 `check-data`: fail on a portal-page URL, on summary text in place of document text, or on a gate rule without a clause id.
3. Task 9: every gap row lists the documents and sections searched and the wording found before the gap claim; the gap register leads the README and the report's findings.
4. Task 12: a Readiness dimension is claimed only with a row of running-system evidence; cut any of 6, 7, 8, 10, 11 that has none.
5. Tasks 11 and 12: one paragraph on what ITU can reuse (manifest schema, clause-tied gate pattern, the Arabic run).
6. Task 10: CLI first; the read-only dashboard is last and optional.
7. Review focus 7: the judge opens the README; are the gaps and the VERIFIED count on the first screen?

## Addendum 2026-10-18 (Fable): from the judging report check

Source: `saudi-judging-patterns-2026-10-17.md` section 9. Five small additions; nothing above is withdrawn.

8. Task 12 and the judge card: a four-row table, final-day lens to evidence. Rows: innovation (gate diff, replay,
   frozen keys), applicability (synthetic UAE operator against the verbatim TDRA text, Arabic run), societal impact
   (the four subscriber harms, each with its clause), responsible AI (CPR 26.7.2 hand-over, 18(4) human review,
   override path). Source of the four words: SPA 2026-09-15, the Saudi final's press description.
9. Addendum item 5, the reuse paragraph, names ITU's announced vehicles (UAE Capacity Building Week page, 2026-10-21):
   SNAI for the Arabic chunks and run, the domain-specific open knowledge base call for the manifest, the global open
   repository of AI agents and metadata for Mizan's agent manifests.
10. Task 9 row shape gains `category`, one of: unclear responsibilities, standards gap, technology gap, legislative
    gap, coordination problem, conflict between objectives (the UAE page's own list, criterion 2).
11. Optional, Task 9: a neighbouring-country example (Saudi CST or PDPL, Qatar CRA) only where a verbatim text is
    already on file. The Build-a-thon 5.0 page asks for it; the UAE page does not.
12. Demo opening (Task 12 drills): one concrete subscriber story before any architecture. Judges' video: "concreteness
    of their solutions", "precise evaluation of market needs".

## Addendum 2026-10-20 (Fable): from the winners' submitted files

Source: `saudi-judging-patterns-2026-10-17.md` section 11 (another team's submitted report and scripts, another team's appendix and
manifest, two new Saudi entries). Item 13 replaces addendum item 1 and the old line 44; the rest add.

13. **Task 2, one status vocabulary.** `status` is text provenance: VERIFIED (text on disk, sha256 matches), REFERENCED
    (URL opened, text not held), UNVERIFIED (asserted, not opened or unpublished), HISTORICAL (superseded). SECONDARY and
    METHOD are gone from `status`: they were binding force, so `binding_status` in {binding, advisory, method} carries
    them (Ethics guideline, Deepfake Guide: advisory; Y.3172, Readiness 2.0, IMDA: method). New column `jurisdiction`
    in {UAE, foreign, international} (EU AI Act, GDPR: foreign). `kb verify` prints the four `status` counts; the
    README's first screen shows VERIFIED / REFERENCED / UNVERIFIED.
14. **Task 2, manifest columns added** (another team): `title_ar`, `is_official_translation`, `url_accessed`, `http_status`,
    `bytes`, `page_count`, `itu_dimensions`, `license_note`, `notes`. Each UAE record's `notes` states which language is
    authoritative where the instrument says so, or "not stated" (the CPR).
15. **Task 2, redistribution.** Full source texts are not committed. `kb fetch` downloads them to `kb/sources/`
    (gitignored) and `kb verify` checks each sha256; where a host blocks, a labelled extract in `kb/extracts/` with its
    URL and the manifest says which text was read live (Sabeeh). Committed: `kb/manifest.csv` and the clause chunks in
    `kb/chunks/` (the quotes the gates need). `license_note` per record. CI runs `kb fetch` before `check-data`;
    if a fetch fails in CI, the test uses the extract and says so.
16. **Task 6, binding only blocks.** `test_block_cites_only_binding_uae_clauses`: every clause id in a `block` or `hold`
    has `binding_status = binding` and `jurisdiction = UAE`; IMDA 2.2.2 and the global examples appear in `reasons[]`
    as `design_basis`, never as the deciding clause. `deny_by_default` keeps IMDA as its design basis and cites licence
    9.1 and CPR 26.7.2 where a human is required.
17. **Tasks 4 and 6, the named override.** `test_override_release_logs_approver_name` (a `hold` released by a human
    writes `actor` = the approver and the release reason); `test_override_refused_on_block` (an override attempt on a
    `block`, such as the model-provider export, is refused and logged with the name that tried).
18. **Task 8, latency split.** Every event records `gate_ms` (decision time) and `model_ms`; `eval` reports median and
    max of both. The report states them in one line (another team: "the verdict lands in 29 milliseconds and the prose
    follows").
19. **Task 9, gap rows gain `kind` and `addressee`.** `kind` in {method, scope, absence, currency} (Sabeeh): gaps 3, 4,
    5 are method; gap 6 scope; gap 7 absence; gap 1 and 2 decided when the row is written. `addressee` names the body
    the recommendation goes to (TDRA, UAE Data Office, the consumer-protection authority, Cabinet), one per row. A gap
    is claimed only where no clause in any VERIFIED or REFERENCED document reaches the concern ("unreached", another team
    D.5); a clause that exists but gives no method is a method gap, not an absence.
20. **Task 9, at least one standards gap** addressed to ITU and stated from the Y.3172 text on disk (candidate: the
    hand-over to a human has no node outcome in the standard). Template section 7 asks for policy gaps and standards
    gaps; the register had only policy.
21. **Task 12, Readiness in three tables** (another team B.1, B.2): the six factors (Report 2.0 p. 17) with documents per
    factor and "supplied by the system" where that is true (sandbox: the governed-versus-ungoverned run; open source:
    the repo and manifest); all thirteen dimensions in three classes: claimed directly with a running-system evidence
    row, evidenced by KB documents only, not claimed. Addendum item 4 still governs the first class: cut any of 6, 7,
    8, 10, 11 without an evidence row. An empty node or cell in the mapping table is written "none found: gap N",
    never left blank (Team Voxel; S2).
22. **Task 12, report shape** copies another team's order inside the template: the first paragraph carries one sourced UAE
    figure (research item 25); the "existing solutions" paragraph names what exists (the OTP/PSCM step for third-party
    charges, CPR 4.11; the IVR hand-over the QoS regulation measures, T1(2a)) and ends in one line: the operator
    already hands the IVR to a human, Mizan makes the chatbot do the same. Named guardrail products only once a
    source is on file. One sentence states the binding-versus-advisory rule (item 16) in another team's words: a departure
    from guidance is never called a violation.
23. **Task 12, video script as a production document** (another team): six beats (the subscriber's story, the KB in Arabic,
    the block, the named override, the hard block with no override, close with gaps and the audit trail and the latency
    line); one block marked cuttable with its word count; a pronunciation and plain-words table (say "the regulator",
    not TDRA, on first use; say "clause", not the number, aloud); an "if something goes wrong" table where the failure
    becomes the point; subtitles checked on three named strings (26.7.2, the two-language quote, the chain hash).
    Rehearse once, timed, before recording.
24. **Task 12, `docs/HOW-IT-WORKS-AR.md`**, the team sheet (another team): Mizan in five sentences, every command and
    screen, the four verdicts in plain words, the five scenarios to memorise, who speaks about what on the final day,
    one opening line in simple English. This closes open item 4 (Rawashdeh's part): the sheet assigns the speaking parts
    once Iyas names them.
25. **Settled 2026-10-20 (Fable), the opening figure:** e& reported **371,476 customer complaints** in its UAE
    operations for the 2025 reporting year (389,387 in 2024; 411,752 in 2023), 88% resolved, 81% first-call resolution.
    Source: e&, *Sustainability Report Appendices 2025*, Appendix 1, "Responsible commercialisation", column
    "YoY data (UAE data)", PDF page 7 (printed 6); `standards-text/eand-sustainability-report-appendices-2025.pdf`,
    SHA-256 `f461044f...27b91c`. Pair it in the same paragraph with the operator's published AI care channel: Etisalat's
    Virtual Assistant, "AI (Artificial Intelligence) powered", 24/7, English or Arabic, app, support site and 101, whose
    listed jobs include "adding or deleting services, changing of packages" and "Billing related clarifications"
    (https://www.eand.ae/en/c/etisalat-virtual-assistant.html, read 2026-10-20). Second sentence, the regulator's own
    count (added the same day, second Perplexity round): "In 2023, the Authority dealt with 23,464 complaints submitted
    by business and home subscribers regarding licensees" (2020 32,998; 2021 29,727; 2022 26,745), TDRA *Sustainability
    Report 2023*, PDF page 34, EN and AR; `standards-text/tdra-sustainability-report-2023-en.pdf`, SHA-256
    `0ac6aa6c...f0a1fa`. It is the latest count TDRA has published (the 2024 and 2025 reports have none, checked).
    Wording rules, each a judge's push-back: "e& UAE" and "2025 reporting year", never "the UAE sector", never "TDRA
    received 371,476"; the two figures have different years and receivers, so no ratio, no "of which", no per-day
    conversion; the fall in either series is not an AI effect (e&'s resolved share also fell, 94 to 88); the assistant
    is "AI-powered", not an agent, launch date unknown. Not the opening: TDRA's 334,116 telemarketing complaints in 2025
    (TDRA Instagram and LinkedIn, 2026-04-01, "violations committed by individuals", Cabinet Resolutions 56 and 57 of
    2024; 48,519 numbers reported, 2,725 violations, AED 15,320,000 fines) goes beside Cabinet 56/2024 wherever the
    report cites the telemarketing rule, scope stated. The TDRA release of 2024-04-02 (AI classifies disputes and
    estimates resolution times in TDRA's own dispute service; about 70% resolved on first contact) and the 2023 report's
    page 35 (closed on time 35% Q4 2022 to 85% Q1 2024; turnaround 14.9 to 10.5 days) go in the "existing solutions"
    paragraph. Press figures citing TDRA (2,900 in Q1 2025; 23,335 for 2023 with the e& and du split; 20,427 January to
    October 2023) are secondary and conflict with TDRA's own table: not in the report. Quotes, hashes and the rejected
    candidates: `perplexity-2026-10-20/opening-figure-read-2026-10-20.md`.
26. **Decided 2026-10-20 (Iyas): DP Technologies reviews.** A real DP Technologies practitioner reads the PDPL steps and
    the scenarios before Task 12, credited in the report by role or name as Iyas chooses, with the correction the review
    produced written down (another team: "whose correction... changed the enforcement model"). Flow: Claude drafts the list of
    proposed changes from research, the reviewer accepts, rejects or fixes each one, and only what the reviewer actually
    changed is credited to them. Person and role: not named yet. Never credit research as a review nobody did.
    Timing: about 2026-11-01, once Tasks 3 and 7 exist; the reviewer reads for about 30 minutes; corrections land before
    Task 12. Nothing goes in on the reviewer's word alone (Iyas, 2026-10-20): every change the reviewer makes is checked
    against the law text in the vault; where both agree it goes in; where it conflicts with a clause, both are shown to
    Iyas and he decides. Until then, Tasks 1 to 11 run as written.
