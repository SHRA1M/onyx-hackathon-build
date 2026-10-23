# Mizan

[![reproduce](https://github.com/SHRA1M/onyx-hackathon-build/actions/workflows/reproduce.yml/badge.svg)](https://github.com/SHRA1M/onyx-hackathon-build/actions/workflows/reproduce.yml)

> **Synthetic data.** The operator, subscribers and numbers in this repo are synthetic. The law texts are real, public, linked and hashed. No consumer data.

## For the reviewer

The four published criteria, each with the one place that shows it:

1. Knowledge base: `kb/manifest.csv` (40 rows, status, sha256, both languages); `python -m onyx kb verify` prints the counts; the downloadable copy is `kb/export/InputDocs/Inputs.md`.
2. Agent capability in error scenarios, and the gaps: `docs/replay/index.html` (five recorded runs, every step with its clause, page and words; no install, no key); the gap register below and `docs/gaps.md`; `docs/replay/whatif-S2-gap-1.md` tests gap 1's recommended rule by replay
3. Auditability: `uv run python -m onyx selftest` recomputes every figure in `docs/report.docx` from the committed hash-chained logs in `runs/`; `uv run python -m onyx replay runs/c5/S2/ar/run1.jsonl` re-decides one run offline.
4. ITU-T Y.3172 and the Readiness Framework: `docs/report.docx`, sections 3 and 4, and the Y.3172 mapping table below.

Mizan puts a consumer on the line. It is a consumer-care AI for a synthetic UAE operator, Team Onyx's entry to the
ITU AI for Good Lab Hackathon UAE 2026 (telecom track): agents propose each step of a chat or call, plain-code gates
written from binding UAE clauses allow or block it, and the same gates run in Arabic and English from the same
clauses. Every step is written to a hash-chained log that replays offline, with the clause, its page and its words.

Team Onyx (BAU Faculty of AI): Iyas Shraim, leader, and three members.

Knowledge base: 36 VERIFIED (text on disk, sha256 matches), 1 REFERENCED (opened, text not held), 3 UNVERIFIED
(asserted, not published; they back no claim) in `kb/manifest.csv`; `python -m onyx kb verify` prints the counts.
[The knowledge base, downloadable](kb/export/InputDocs/Inputs.md): one record per document with its sha256 and link;
16 rows link a landing page because the document link could not be verified. The Telecommunications Law 3/2003 is
read from the federal legislation portal's consolidated texts, English and Arabic; Arabic prevails, Arabic Articles 13,
14 and 72 to 79 bis were read from page images, and Art 14(3) is quoted from the Arabic because the portal's English
mistranslates it (manifest notes).

## Why

e& reported 371,476 customer complaints in its UAE operations for 2025
([e&, Sustainability Report Appendices 2025](https://www.eand.com/content/dam/eand/assets/docs/sustainability/2025/eand-sustainability-report-appendices.pdf),
Appendix 1, PDF page 7). TDRA dealt with 23,464 complaints about licensees in 2023, the latest count it has published
([TDRA, Sustainability Report 2023](https://tdra.gov.ae/-/media/Media/Press-Kit/Sustainability-Report/EN/Sustainability-report-2023-English.ashx),
p. 34). At the operator the first contact is already an AI:
[Etisalat's Virtual Assistant](https://www.eand.ae/en/c/etisalat-virtual-assistant.html), "AI (Artificial
Intelligence) powered", 24/7, English or Arabic, whose listed jobs include "adding or deleting services, changing of
packages" and "Billing related clarifications". No source on file says what stops such an AI when a chat becomes a
complaint or a disconnection. The binding texts do, and Mizan's gates are written from them.

## Three things to look at first

![S2 step 3: the gate blocks the agent's reply and hands the complaint to a person, citing CPR 26.7.2, p. 65](docs/replay/screenshots/S2-step3-en.png)

- A consumer on the line: five scenarios of a subscriber in a chat or call, not an institution in a drill.
- Gates from binding UAE clauses: every allow and block names the clause, its page and its words, in `docs/replay/`.
- Arabic parity: the same gates and keys in both languages, action recall 0.96 English / 0.94 Arabic on C5 (`eval/results.md`).

## Gap register

Nine rows, generated from `onyx/data/gaps.json` by `python -m onyx gaps`; each row's clauses searched, both languages, global quotes and recommendation are in [`docs/gaps.md`](docs/gaps.md). Gap 1 is also tested, not only stated: `uv run python -m onyx whatif runs/c5/S2/run1.jsonl --rule gap-1` replays the recorded S2 run under the rule the register recommends (proposed, not law): the held step S2-5 is released, the hand-over duty gains a two-minute clock, and one new finding appears: the rule needs the hand-over time recorded, which this log does not carry. Page: `docs/replay/whatif-S2-gap-1.md`.

<!-- gap-register:start -->
| id | gap | kind | category | addressee | global example | exposed by |
| --- | --- | --- | --- | --- | --- | --- |
| gap-1 | Complaint hand-over: the trigger and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1); the mechanics are not (stop, hand over, how fast), and QoS T1(2a) measures only the wait after the IVR choice. | method | standards gap | TDRA | IMDA 2.2.2; IMDA 2.4.2 | S2-3 |
| gap-2 | Consent elicited by an AI: the CPR medium classification (4.10, 4.17, 4.22) decides whether an OTP is needed, and PDPL 6(1)(b) names consent 'in writing or electronically', not spoken. | method | coordination problem | TDRA, UAE Data Office | EU AI Act Art 50(1); IMDA 2.2.2 | S1-4 |
| gap-3 | 'Adequate verification process' (CPR 24.10) is undefined for a remote channel; the Electronic Transactions Art 33 trust levels were never mapped to it. | method | standards gap | TDRA | eIDAS Art 8(1); eIDAS Art 8(3)(c) | S5 (verification step) |
| gap-4 | Automated disconnection: PDPL 18(4) human review has no procedure, deadline or regulator; the 18(2) contract escape is undercut by Cabinet 66/2023 34(1), (3), (5) (inferred interaction, both quoted). | method | unclear responsibilities | UAE Data Office | GDPR Art 22(3) | S4-4, S4-5 |
| gap-5 | Subscriber data to a hosted model provider: the rule is present (PDPL 7(5), 8(1), 13(2), 23(1)(a), licence 3.4.1), the machinery absent (the Art 22 list, 23(2), 8(11)). | method | legislative gap | UAE Data Office | GDPR Art 28(3)(a); GDPR Art 45(1) | S3-3 |
| gap-6 | AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) makes it a validity condition for sales only. | scope | legislative gap | Cabinet | EU AI Act Art 50(1); EU AI Act Art 50(5); EU AI Act Art 113 | S1-3 |
| gap-7 | No binding UAE text sets conduct standards for an AI agent dealing with a consumer. The clauses that name AI or an automated agent set a charge waiver (CPR 25.14.1), a bar (26.7.2), a definition (Spam Calls v4 3.3(iii)), a permission (Cabinet 56/2024 5(6)) and a tool (Child Digital Safety 10(1)(g)); PDPL 18 and Electronic Transactions 11 to 13 govern automated decisions and contracts as outcomes, not the agent's conduct. | absence | standards gap | TDRA | IMDA 2.1.2 | all |
| gap-8 | Standards gap, addressed to ITU: Y.3172 has no node outcome for a hand-over to a human. The policy node applies policies to the model's output and the distributor sends it on to a sink that acts; no node routes it to a person. | absence | standards gap | ITU | none; the recommendation is the example | S2-3 |
| gap-9 | A child on the line: the Child Digital Safety Law 26/2025 makes the caregiver sign the service terms where the beneficiary is a child (11(1)(b)) and requires verified caregiver consent for under-13 data (7(1)), but the Cabinet classification (Art 6), the TDRA instructions to providers (Art 11) and the penalties (Art 16) are unpublished, and no text addressed to a telecom provider says how an automated channel learns that the person is a child. | method | legislative gap | TDRA, Cabinet | 16 CFR 312.5(a)(1); 16 CFR 312.5(b)(1) | mapping (SRC, P); U2 (drill bank, not run) |
| candidate-4-4-fixed-term-bundle | Whether an expired fixed-term bundle is an 'existing Service... extended or renewed' under CPR 4.4. | scope | legislative gap | TDRA | none on disk | S1-6 |
| candidate-79bis-2-fine-schedule | The Cabinet schedule of licensee violations and fines that Telecom Law 79 bis (2) promises (fines up to AED 10,000,000 a violation) is not published; the only published telecom fine schedule, Cabinet 57/2024, covers the Telemarketing Regulations. Until it exists, a CPR breach by an automated channel sits in the 79 bis (1) and licence 16.3.2 band, AED 50,000 to 200,000, doubled under licence 16.3.3 for repetition, a missed date or a material failure. | absence | legislative gap | Cabinet | none (order Task 15: no global example) | mapping (P) |
<!-- gap-register:end -->

The global quotes are checked verbatim offline against the fetched texts in `kb/sources/global/` (not committed,
addendum item 15); CI checks every UAE quote against the committed chunks and the register's structure.

## Run it without a key

No API key and no model call. CI runs every line on each push.

```
git clone https://github.com/SHRA1M/onyx-hackathon-build.git
cd onyx-hackathon-build
uv sync
uv run python -m onyx selftest
uv run python -m onyx replay runs/c5/S1/run1.jsonl
uv run python -m onyx replay runs/c5/S2/ar/run1.jsonl
uv run pytest -q
```

`selftest` runs scenario S1 through the agents and the gate on a scripted model, checks the log's hash chain, replays
it, prints the headline figures and recomputes them from the committed logs. `replay` re-decides a recorded live run
offline and prints the complaint hand-over in S2 with CPR 26.7.2 and licence 9.1 in English and Arabic.

Replay viewer: open `docs/replay/index.html` in a browser (no server, no key).

## Scenarios

Each page is generated by `python -m onyx replay-page` from the one recorded governed run named beside it: a C5 run
(prompt v5), the first English one that cites the clauses the scenario is grounded in. S2 reads the first C5 run whose
step 3 carries the hand-over with both quotes and whose step 4, the human's, is allowed (an Arabic run; neither C5
English run allowed step 4). S1 stays on C3's first English run: no recorded run, C3 or C5, cites CPR 17.4 or 17.4.1.

| id | scenario | steps | replay page | run read | grounded in |
| --- | --- | --- | --- | --- | --- |
| S1 | Roaming before a flight | 6 | [docs/replay/S1.md](docs/replay/S1.md) | `runs/S1/run1.jsonl` | `tdra-cpr-v2-en:17.4` (p. 51), `tdra-cpr-v2-en:17.4.1` (p. 51) |
| S2 | A billing question becomes a complaint | 6 | [docs/replay/S2.md](docs/replay/S2.md) | `runs/c5/S2/ar/run1.jsonl` | `tdra-cpr-v2-en:4.20.1` (p. 17) |
| S3 | A partner wants the data, and the model provider is abroad | 5 | [docs/replay/S3.md](docs/replay/S3.md) | `runs/c5/S3/run1.jsonl` | `pdpl-45-2021-en:23(1)` (p. 25) |
| S4 | Non-payment: an automated disconnection | 5 | [docs/replay/S4.md](docs/replay/S4.md) | `runs/c5/S4/run1.jsonl` | `tdra-cpr-v2-en:22.1.1` (p. 58) |
| S5 | A TDRA dispute and a loss report | 6 | [docs/replay/S5.md](docs/replay/S5.md) | `runs/c5/S5/run1.jsonl` | `decision-16-2026-ar:4.18` (p. 10), `tdra-cpr-v2-en:26.11` (p. 66) |

## Y.3172 mapping

The nodes of ITU-T Y.3172 (06/2019) clause 8.1, with the MLFO and the ML sandbox, as Mizan implements them.

| node | in Y.3172 | in Mizan | where |
| --- | --- | --- | --- |
| SRC | source of data | the scenario injects and the KB sources | `onyx/data/scenarios/`, `kb/manifest.csv` |
| C | collector | each agent's inbox: the coordinator releases a step only to the agent it names | `onyx/coordinator.py` |
| PP | preprocessor | clause chunking and mandate-scoped retrieval | `onyx/kb.py`, `onyx/agents/base.py` |
| M | model | the model behind one OpenAI-compatible adapter; it proposes, never decides | `onyx/model.py` |
| P | policy | the gates, plain code written from binding UAE clauses | `onyx/gate.py` |
| D | distributor | coordinator routing, the human hand-over and the deadlines the gates set | `onyx/coordinator.py` |
| D, hand-over outcome | none found: gap-8 | Y.3172 gives no node outcome that sends an output to a human; Mizan adds it at D | `docs/gaps.md` (gap-8) |
| SINK | sink | the hash-chained audit log, the gap register, the replay pages | `onyx/audit.py`, `docs/gaps.md`, `docs/replay/` |
| MLFO | ML function orchestrator | the coordinator's staged release of steps | `onyx/coordinator.py` |
| ML sandbox | ML sandbox | the governed-versus-ungoverned run on the same scenarios | `runs/ungoverned/`, `eval/results.md` |

## What we do not claim

- The answer keys are ours, written and hashed before the first live run (`onyx/data/keys/HASHES.txt`).
- The humans in the recorded runs (approvers, override attempts) are scripted steps, not people.
- UNVERIFIED rows in the manifest back no claim.
- No source on file shows how a UAE operator's assistant is governed; the Etisalat Virtual Assistant page lists what it does, not what stops it.

## Model

- Model: `claude-sonnet-5-5`, through Anthropic's OpenAI-compatible endpoint `https://api.anthropic.com/v1/`
  (`onyx/model.py`, one adapter for every model).
- Prices: https://platform.claude.com/docs/en/about-claude/pricing, read 2026-10-21 (`onyx/data/model_prices.json`).
- Bake-off: [`eval/bakeoff.md`](eval/bakeoff.md), one governed run per scenario (S1 to S5) per language per model.
- Scored run: [`eval/results.md`](eval/results.md), C5, Sonnet on prompt v5, two runs per scenario per language,
  governed (English / Arabic): action recall 0.96 / 0.94, citation validity 0.99 / 1.00, obligation proxy
  0.57 / 0.56; 5 of 112 key steps missed.
- Ungoverned baseline: C3, Sonnet on prompt v3, three runs per scenario per mode per language.

Clause-id resolution (2026-10-21, hq): a cited id missing its language ending (`-en`, `-ar`) resolves to the one
clause given to that agent for that step that it names, never to the whole knowledge base and never when two match;
in C3 and C4 S1 that was 6 ids in 4 of 389 proposals citing a clause.

The adapter takes any OpenAI-compatible endpoint; a UAE-hosted Jais 3 or Falcon-H1 Arabic served through vLLM
exposes the same API, so the provider is three values in `.env`.

Bake-off rows (English / Arabic), copied from `eval/bakeoff.md`:

| Row | Opus 5.5 v1 | Sonnet 5.5 v1 | Haiku 5.5 v1 | Sonnet 5.5 v2 | Haiku 5.5 v2 |
|---|---|---|---|---|---|
| Citation validity | 1.00 / 0.88 | 1.00 / 1.00 | 0.97 / 0.97 | 0.97 / 1.00 | 0.92 / 0.95 |
| Action recall | 0.29 / 0.10 | 0.43 / 0.17 | 0.47 / 0.32 | 0.70 / 0.48 | 0.45 / 0.39 |
| Obligation proxy | 0.10 / 0.04 | 0.17 / 0.23 | 0.17 / 0.16 | 0.23 / 0.35 | 0.23 / 0.29 |
| Gap recall | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.47 / 0.00 | 0.20 / 0.00 |
| JSON parse failures | 18 of 26 / 20 of 26 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| Replies stopped by the endpoint | 18 of 26 / 20 of 26 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| Cost, 10 runs (USD) | 0.91 | 0.63 | 0.04 | 0.86 | 0.05 |

Prompt v1 is commit d85871d, v2 is a8f4acb. In v2 the Arabic gap ids were present in the replies' notes in 10 of
10 runs but scored 0; prompt v3 asks for them as `flag_gap` proposals.

With prompt v1, the endpoint stopped 38 of 52 Opus replies (content_filter). With prompt v2, which renamed the
`reasoning_chain` field and added instructions and clause text, 0 of 10 were stopped
(`runs/opus-filter-v2/S2/run1.jsonl`, `runs/opus-filter-v2/S2/ar/run1.jsonl`). The cause is not isolated. Where a
reply was stopped, the adapter recorded the reason, the reply proposed nothing, the gate saw no malformed action,
and the run went on.

## Setup from a fresh clone

Needs [uv](https://docs.astral.sh/uv/).

```
uv venv --python 3.12
uv pip install -e ".[dev]"
uv run pytest
uv run python -m onyx --help
```

## Licence

Code: MIT (see `LICENSE`). Knowledge-base documents remain their publishers'.
