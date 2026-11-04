# Mizan

[![reproduce](https://github.com/SHRA1M/onyx-hackathon-build/actions/workflows/reproduce.yml/badge.svg)](https://github.com/SHRA1M/onyx-hackathon-build/actions/workflows/reproduce.yml)

> **Synthetic data.** The operator, subscribers and numbers in this repo are synthetic. The law texts are real, public, linked and hashed. No consumer data.

## For the reviewer

The five published criteria, each with its evidence and one way to check it:

| Criterion | Evidence | How to check it |
|---|---|---|
| Knowledge base | `kb/manifest.csv` (108 rows, status, sha256, both languages); the downloadable copy `kb/export/InputDocs/Inputs.md`; what it holds and its limits: `kb/DATASHEET.md`; retrieval measured on its own, no model: `eval/results.md`, section "Retrieval alone" | `uv run python -m onyx kb verify` prints the counts |
| Agent capability in error scenarios | `docs/replay/index.html` (five recorded runs, every step with its clause, page and words; no install, no key) | `uv run python -m onyx why runs/c5/S2/run1.jsonl --step 3` explains one step from its log |
| Policy, strategy and standards gaps | the gap register below and `docs/gaps.md`; `docs/replay/whatif-S2-gap-1.md` tests gap 1's recommended rule by replay | open `docs/gaps.md` |
| Auditability | the committed hash-chained logs in `runs/`; `docs/report.pdf` | `uv run python -m onyx selftest` recomputes the report's figures from `runs/` |
| ITU-T Y.3172 and the Readiness Framework | `docs/report.pdf`, the Requirements and Mapping sections | [the Y.3172 diagram and mapping table below](#y3172-mapping) |

The report's annex (data and model, clause to code, the governed test, what ITU can reuse) is in `docs/report.pdf` after page 5.

Mizan puts a consumer on the line. It is a consumer-care AI for a synthetic UAE operator, Team Onyx's entry to the
ITU AI for Good Lab Hackathon UAE 2026 (telecom track): agents propose each step of a chat or call, plain-code gates
written from binding UAE clauses allow or block it, and the same gates run in Arabic and English from the same
clauses. Every step is written to a hash-chained log that replays offline, with the clause, its page and its words.

Team Onyx (BAU Faculty of AI): Iyas Shraim, leader, Mohammed Rawashdeh and Yanal Faouri.

Knowledge base: 100 VERIFIED (text on disk, sha256 matches), 5 REFERENCED (opened, text not held), 3 UNVERIFIED
(asserted, not published or not reached; they back no quoted clause; two of them record an absence (the PDPL Executive Regulations, the agentic framework text) that the register claims from the portal check written in the row, dated) in `kb/manifest.csv`; `python -m onyx kb verify` prints the counts.
[The knowledge base, downloadable](kb/export/InputDocs/Inputs.md): one record per document with its sha256 and link;
22 rows link a landing page because the document link could not be verified. The Telecommunications Law 3/2003 is
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
- Arabic parity: the same gates and keys in both languages, action recall 0.96 English / 1.00 Arabic on C5 (`eval/results.md`).

## Gap register

Fifteen rows, generated from `onyx/data/gaps.json` by `python -m onyx gaps`: eleven in the report's table for room, gap 7 and gaps 13 to 15 in Annex F, and two candidates; each row's clauses searched, both languages, global quotes and recommendation are in [`docs/gaps.md`](docs/gaps.md). The three GCC telecom consumer regulations read (Saudi 2024, Qatar 2024, Kuwait 2022) name no AI channel, hand-over clock, machine disclosure or Arabic quality measure either; Saudi 552/1445 comes nearest, requiring a route to an employee and a qualified employee on every complaint. Gap 1 is also tested, not only stated: `uv run python -m onyx whatif runs/c5/S2/run1.jsonl --rule gap-1` replays the recorded S2 run under the rule the register recommends (proposed, not law): the held step S2-5 is released, the hand-over duty gains a two-minute clock, and one new finding appears: the rule needs the hand-over time recorded, which this log does not carry. Page: `docs/replay/whatif-S2-gap-1.md`.

The model can also die, and the gate still decides: `uv run python -m onyx model-down runs/c5/S2/run1.jsonl --at 3` replays the recorded S2 run with the model call at step 3 made to fail (fault injection: the model call is made to fail at this step; nothing else changes). The care agent's step logs `model_unavailable`, the coordinator authors an `escalate_to_human` proposal in plain code, and the gate's deny-by-default hold hands the conversation to Human agent H-01, the same named human the recorded run reaches. No model takes part in that step; every later decision keeps its verdict. A live run takes the same path when a real model fails after its last retry, instead of crashing. Page: `docs/replay/model-down-S2.md`.

Two UAE free zones have their own data protection law: DIFC Law 5/2020 binds Controllers and Processors 'incorporated in the DIFC, regardless of whether the Processing takes place in the DIFC or not' (Art 6(3)(a)), and the ADGM Data Protection Regulations 2021 apply 'in the context of the activities of an Establishment of a Controller or a Processor in ADGM' (s. 3(1)). A federal telecom licensee outside the zones is not within either. Where a free-zone text fills a federal gap, the row names it as a UAE free-zone example, never as a federal rule.

The PDPL names the UAE Data Office (Art 24). On 2026-06-14 the Prime Minister approved an Artificial Intelligence and Data Authority, reporting to the Cabinet, that 'will bring together under one mandate the functions previously held by three separate entities', the Data Office among them (WAM, 14 June 2026, `https://www.wam.ae/en/article/c0pz7ku-mohammed-bin-rashid-approves-establishing`; manifest rows `wam-2026-06-14-ai-data-authority` and, in Arabic, `fed-ai-data-authority-2026-06-14`). No establishing instrument was found on the official portal on 2026-11-02, and dataoffice.gov.ae did not resolve on 2026-11-02. The register keeps the PDPL's name.

The federal Official Gazette (Ministry of Justice, elaws.moj.gov.ae) was unreachable on 2026-11-02, 2026-11-03 and 2026-11-04 (curl and Chrome from hq, GitHub answering as the control), so its issues were not swept; the legislation portal, which lists each law's Gazette number and its regulations, is the official check, and it publishes no issue archive; the newest issue the portal names is No. 833 of 14 October 2026 (entry 4660, read 2026-11-04).

<!-- gap-register:start -->
| id | gap | kind | category | addressee | global example | exposed by |
| --- | --- | --- | --- | --- | --- | --- |
| gap-1 | Complaint hand-over: the trigger and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1) and the complaint has clocks (acknowledge at once by telephone, 26.13.3; conclude in twenty business days, 26.14.2); the transfer has none: what the agent does when the conversation turns, when the human is in it, whether the time is recorded. QoS T1(2a) measures only the wait after the IVR choice. | method | standards gap | TDRA | IMDA 2.2.2; IMDA 2.4.2; DSA 2022/2065 Art 12(1); Spain Ley 10/2025 Art 8(2); Spain Ley 10/2025 Art 8(3); Saudi CST 552/1445 §13.1.1; Saudi CST 552/1445 §13.1.2; Saudi CST 552/1445 §26.5.2; India TRAI TCCRR 2012 reg 3(9); India TRAI TCCRR 2012 reg 3(9), proviso; India TRAI TCCRR 2012 new reg 3(9)(d); India TRAI TCCRR 2012 new reg 3(9)(e); India TRAI TCCRR 2012 new reg 3(3), first proviso | S2-3 |
| gap-2 | Consent elicited by an AI: the CPR accepts spoken consent if it can be stored (4.7.2) and sets the consent safeguard by sales medium: a recording of the Subscriber giving verbal consent on a call to the call centre (4.17.3), a 'no' default on yes/no screens in the Licensee App (4.22.3), 2FA for each online purchase (4.23.2), and 2FA in all digital applications unless expressly specified otherwise (4.10); none names an AI channel, so the safeguard an agent must meet follows the channel the operator embeds it in (a voice agent on the call-centre line reads as 4.17, a chat agent in the app as 4.22 or 4.10, a web chat as 4.23), not what the agent does; the PDPL permits the processing the contract needs without consent (4(9)) and wants any further processing consented 'in writing or electronically' (6(1)(b)); one spoken 'yes' buys the service and consents to nothing beyond it, and whether a 'yes' the agent itself heard and interpreted is the Subscriber's positive affirmative action taken freely (4.7.1), or consent in writing or electronically under 6(1)(b), is unsaid. | method | coordination problem | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2; Singapore ETA s. 15; Saudi CST 552/1445 §5.1.2; Saudi CST 552/1445 §5.1.3 | S1-4 |
| gap-3 | 'Adequate verification process' (CPR 24.10) is undefined for a remote channel; no published text maps the Electronic Transactions Art 33 trust levels to it (portal and TDRA site checked 2026-11-02 and 2026-11-04). | method | standards gap | TDRA | eIDAS Art 8(1); eIDAS Art 8(3)(c); 47 CFR 64.2010(b); Qatar CCPR 2024 §1.2 (Customer Consent); Saudi CST 552/1445 §10.7 | S5 (verification step) |
| gap-4 | Automated disconnection: the PDPL 18(4) human review has no procedure or deadline; the only route is a complaint to the Data Office (Art 24), which has no clock either (Art 25's 30 days apply to grievances against the Office's own decisions). | method | unclear responsibilities | UAE Data Office | GDPR Art 22(3); GDPR Art 12(3); DSA 2022/2065 Art 20(6) | S4-4, S4-5 |
| gap-5 | Subscriber data to a hosted model provider: the rule is present (PDPL 7(5), 8(1), 13(2), 23(1)(a), licence 3.4.1), the machinery absent (the Art 22 list, 23(2), 8(11)). | method | legislative gap | UAE Data Office | GDPR Art 28(3)(a); GDPR Art 45(1); DIFC DP Regulations (UAE free zone, not federal) Regulation 5; DIFC DP Regulations (UAE free zone, not federal) Appendix 3 | S3-3 |
| gap-6 | AI disclosure: no federal duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) asks only that the person 'knows, or is supposed to know, that such system will make or execute the contract automatically'. | scope | legislative gap | Cabinet | Maine §1500-DD(2); California BPC §17941(a); California BPC §17941(b); EU AI Act Art 50(1); EU AI Act Art 50(5); EU AI Act Art 113; DIFC DP Regulations (UAE free zone, not federal) Regulation 10.2.2(a); Maine title page; India TRAI TCCRR 2012 new reg 3(3), second proviso | S1-3 |
| gap-7 | No binding federal text sets conduct standards specific to an AI agent dealing with a consumer: CPR 3.3's duty of fairness and accurate information is general; Trade Law 14/2023 names AI in its definition (Art 1) and bars misleading dealing (Art 5(7)); nothing names disclosure, limits, escalation or a hand-over for an automated agent. | absence | standards gap | TDRA | Utah Code 13-77-102; Moffatt v. Air Canada 2024 BCCRT 149 para 27; Moffatt v. Air Canada 2024 BCCRT 149 para 28; India TRAI TCCRR 2012 reg 3(9); India TRAI TCCRR 2012 reg 3(9), proviso; California HSC §1339.75(a)(1)(C); California HSC §1339.75(a)(2); DIFC DP Regulations (UAE free zone, not federal) Regulation 10.2.2(a); DIFC DP Regulations (UAE free zone, not federal) Regulation 10.2.2(b)(ii); DIFC DP Regulations (UAE free zone, not federal) Regulation 10.2.2(d); India TRAI TCCRR 2012 new reg 3(3), third proviso; India TRAI TCCRR 2012 new reg 3(9)(d) | all |
| gap-8 | Standards gap, addressed to ITU: Y.3172 has no node outcome for a hand-over to a human. The policy node applies policies to the model's output and the distributor sends it on to a sink that acts; no node routes it to a person. | absence | standards gap | ITU | 3GPP TS 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4; ITU-T F.748.67 RQR-001; ITU-T F.748.67 OMR-010 | S2-3 |
| gap-9 | A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the Art 11 instructions to providers and the Art 16 penalties are unpublished, and Cabinet Resolution 106/2026's age checks reach social media platforms only (Art 2); nothing says how a telecom channel learns the person is a child. | method | legislative gap | TDRA, Cabinet | 16 CFR 312.5(a)(1); 16 CFR 312.5(b)(1) | mapping (SRC, P); U2 (drill bank, not run) |
| gap-10 | Arabic on an automated channel: the texts set the language (CPR 3.2.2: written information in Arabic or English as the Consumer prefers, both if unknown; Consumer Law 26: data, advertisements and contracts in Arabic; 8(4): the invoice in Arabic; Cabinet 66/2023 Annex 2: AED 100,000 for each) and none sets the quality: no binding text requires an automated channel to answer as well in Arabic as in English, and the QoS Policy v3.0 has no indicator per language. | method | standards gap | TDRA | Canada OLA s. 22; Canada OLA s. 26; Canada OLA s. 27; Wales WLS Standard 15; Wales WLS Standard 22; Wales WLS Standard 60 | C5 per-language scoring (M, D nodes); mapping (SRC) |
| gap-11 | A misheard or misread order: the CPR defaults an on-screen yes/no to 'no' to avoid an accidental 'yes' (4.22.3, 4.23.3), requires an OTP for each online purchase (4.23.2) and a recording of verbal consent on telephone sales (4.17.3); no text says what a voice or chat channel must do when it interprets the subscriber's words itself, so 'don't add it' heard as 'add it' reaches the OTP step without being read back. | method | standards gap | TDRA | E-Commerce Dir. 2000/31 Art 11(2); CRD 2011/83 Art 8(2); US TSR 16 CFR 310.3(a)(3)(ii); Qatar 16/2010 Art 56(1); Qatar 16/2010 Art 19 | mapping (P); S1 step 3 (bundle offered, hold until the OTP and the consent form) is the step where the rule would apply; not in a recorded run. |
| gap-12 | Standards gap, addressed to ITU. Mapped first: Mizan's stop at S2-3 sits at Y.3173 'Human and System' on the decision step (7.2, Table 7-1, p. 6: "a) Human; b) Human and System; c) System."), and its hand-over is Readiness 2.0 D9's inference-to-action latency in the other direction (p. 27: "inference-to-action latency: average time from first inference to human action"; there the AI alerts and the human acts). Readiness 2.0 also measures the human shaping the inference (D8, p. 25) and states that accountability of final decisions remains with humans (D10, p. 29). Mapped there, neither text measures when an acting agent must stop or how long the hand-over takes; ITU-T F.746.16 11.2 measures how often (a manual intervention rate, graded so that less intervention scores a higher level, no threshold), the opposite direction to a regulator's floor such as CPR 26.7.2; ITU-T F.748.67 CRR-003 measures the queue after the transfer, not the time to it. Y.3173 Table 7-2 NOTE 1 (p. 7) gives a human's order the highest authority ("decisions and execution instructions provided by a human being have the highest authority"); it never requires the system to ask. Y.3173 reproduces SAE J3016's levels in Appendix I (Table I.1), the request to intervene included, and carries no fallback dimension into its own Table 7-1. | absence | standards gap | ITU | SAE J3016 (Y.3173 Table I.1) level 3; SAE J3016 (Y.3173 Table I.1) level 4; EU Roaming Reg 2022/612 Art 14(4); EU Roaming Reg 2022/612 Art 14(4), last subparagraph; EU AI Act Art 14(4)(e) | S2-3 (the complaint hand-over, CPR 26.7.2) |
| gap-13 | PDPL 9(1) and 9(2) make the Controller notify the Data Office and the data subject of a breach 'within the period and in accordance with the measures and requirements set by the Executive Regulations'. Art 28 gave the Council of Ministers six months from 20 Sep 2021 to issue them, on the Bureau's proposal. On 2026-11-02 the official portal lists no Executive Regulations of this Decree-Law, in either language, so no period exists in any published federal text; an operator's AI that detects a breach has no clock to run. | absence | legislative gap | Council of Ministers, UAE Data Office (proposer, Art 28) | GDPR Art 33(1); ADGM DPR 2021 (UAE free zone, not federal) s. 32(1); DIFC DP Law 5/2020 (UAE free zone, not federal) Art 41(1) | mapping (P) |
| gap-14 | The Controller appoints a Processor with sufficient guarantees (7(5)) and the Processor follows its instructions (8(1)); where several Processors take part, 8(10) asks only for a written contract among them, and no clause asks for the Controller's authorisation before a Processor brings in another. 8(11) leaves processor standards to the Executive Regulations, which the portal does not list on 2026-11-02. No Data Office, Cabinet or Executive-Regulation instrument on sub-processors was found (portal, both languages; Perplexity 2026-11-02 found none). | absence | legislative gap | Council of Ministers (Executive Regulations, 8(11), 28), UAE Data Office (proposer) | GDPR Art 28(2); ADGM DPR 2021 (UAE free zone, not federal) s. 26(2); DIFC DP Law 5/2020 (UAE free zone, not federal) Art 24(2) | S3-4 |
| gap-15 | The Cabinet schedule of licensee violations and fines that Telecom Law 79 bis (2) promises (fines up to AED 10,000,000 a violation) is not published; the only published telecom fine schedule, Cabinet 57/2024, covers the Telemarketing Regulations. Until it exists, a CPR breach by an automated channel sits in the 79 bis (1) and licence 16.3.2 band, AED 50,000 to 200,000, doubled under licence 16.3.3 for repetition, a missed date or a material failure. The Cabinet has issued itemised schedules under three neighbouring laws (57/2024 telemarketing, 52/2024 trust services, 200/2025 digital trade); none under 79 bis (2). On 2026-11-02 the portal's Telecommunication, Technology and Space sector lists 12 instruments (14 in Arabic), none a schedule of telecom licensee fines; the Regulation Table of Decree-Law 3/2003 shows no records. The Cabinet has issued such a schedule for the space sector (Cabinet Resolution 206/2025, 'Regulations of Violations and Administrative Penalties... Space Activities'), not for telecommunications. | absence | legislative gap | Cabinet | Ofcom Penalty Guidelines 2017 1.11; Ofcom Penalty Guidelines 2017 1.2 | mapping (P) |
| candidate-4-4-fixed-term-bundle | Whether an expired fixed-term bundle is an 'existing Service... extended or renewed' under CPR 4.4. | scope | legislative gap | TDRA | EECC 2018/1972 Art 105(3); TKG 2021 § 56(3) | S1-6 |
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
uv run python -m onyx why runs/c5/S3/run1.jsonl --step 3
uv run pytest -q
```

`selftest` runs scenario S1 through the agents and the gate on a scripted model, checks the log's hash chain, replays
it, prints the headline figures and recomputes them from the committed logs. `replay` re-decides a recorded live run
offline and prints the complaint hand-over in S2 with CPR 26.7.2 and licence 9.1 in English and Arabic. `why` explains one recorded step from its log: verdict, clauses with their words, hand-over, event hash.

Replay viewer: open `docs/replay/index.html` in a browser (no server, no key).

Demo, four steps (the report's Demo scenarios; every one a replay or plain code over the committed logs, no key):

1. Online: the five recorded scenarios, every step with clause, page and words: `docs/replay/index.html`.
2. The subscriber asks why: `uv run python -m onyx why runs/c5/S3/run1.jsonl --step 3` (add `--lang ar` for Arabic) prints the verdict, each clause with its title, page and words, the hand-over and the event hash, from the log alone.
3. Conflicting advice: S3 step 3, the gate blocks the transfer abroad (PDPL 22, 23(2)) and refuses the override (`override_refused`): `docs/replay/S3.md`, step 3.
4. Another body, another rule: `uv run python -m onyx whatif runs/c5/S2/run1.jsonl --rule gap-1` (TDRA, `docs/replay/whatif-S2-gap-1.md`) and `--rule gap-4` on `runs/c5/S4/run1.jsonl` (UAE Data Office, `docs/replay/whatif-S4-gap-4.md`); a replay costs USD 0, a live C5 run USD 0.27 (`eval`: USD 5.3767 over 20 runs).

## Open the site

Open `docs/site/index.html` from disk: six pages, no server, no network, no key. The overview's figures come from
`eval/results.json`, the runs page is the replay viewer, the gap register and the knowledge base are rendered from
`onyx/data/gaps.json` and `kb/manifest.csv`, and "Verify a log" recomputes the hash chain of any C3, C4 or C5 run in
the browser. `python -m onyx site` writes it; CI fails if a byte differs. From 2026-11-09 GitHub Pages serves
`docs/site/`.

![The site's overview: the C5 and C3 figures, read from eval/results.json](docs/site/screenshots/index.png)

![Verify a log: every event's hash recomputed in the browser, chain ok](docs/site/screenshots/verify.png)

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

The seven unseen scenarios (`onyx/data/scenarios/unseen/`, U1 to U7) were written before the first scored run, their bytes fixed by commit 93a7d40 (2026-10-21) and unchanged since; none has been sent to a model. Their cold runs are a next step.

## Y.3172 mapping

```mermaid
flowchart TD
    %% Convention: solid edge, used on every recorded run; dotted edge, used only by an optional step.
    %% An arrow means the file at its tail calls or imports the file at its head.
    subgraph n_src["SRC"]
        scenarios["Scenarios<br/>onyx/data/scenarios/"]
    end
    subgraph n_mlfo["MLFO"]
        mlfo["Staged release of steps<br/>onyx/coordinator.py"]
    end
    subgraph n_c["C"]
        collector["Each agent's inbox<br/>onyx/coordinator.py"]
    end
    subgraph n_pp["PP"]
        base["Mandate-scoped retrieval<br/>onyx/agents/base.py"]
        kb["Clause chunks<br/>onyx/kb.py"]
    end
    subgraph n_m["M"]
        model["Model adapter<br/>onyx/model.py"]
    end
    subgraph n_p["P"]
        gate["Gates<br/>onyx/gate.py"]
    end
    subgraph n_d["D"]
        dist["Routing and hand-over<br/>onyx/coordinator.py"]
    end
    subgraph n_sink["SINK"]
        audit["Hash-chained log<br/>onyx/audit.py"]
    end
    subgraph n_sandbox["ML sandbox"]
        runs["Recorded runs<br/>onyx/runs.py"]
        eval["Scoring<br/>onyx/eval.py"]
        whatif["What-if replay<br/>onyx/whatif.py"]
        modeldown["Model-down replay<br/>onyx/modeldown.py"]
        localmodel["Local-model page<br/>onyx/localmodel.py"]
    end
    %% The one edge that is a read, not a call or an import: scenario files, read through onyx/data.py.
    scenarios --> mlfo
    mlfo --> collector
    collector --> base
    collector --> dist
    base --> kb
    base --> model
    base --> audit
    dist --> gate
    dist --> audit
    gate --> kb
    runs --> mlfo
    runs --> model
    eval --> audit
    kb -. "kb fetch" .-> kb
    whatif -.-> mlfo
    whatif -.-> gate
    whatif -.-> model
    modeldown -.-> mlfo
    modeldown -.-> whatif
    modeldown -.-> model
    localmodel -.-> runs
```

Solid edge: used on every recorded run. Dotted edge: used only by an optional step: `whatif`, `model-down`, `kb fetch`, and `localmodel` (a page, recorded by `scripts/demo_local.py`).

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
| MLFO | ML function orchestrator | the coordinator's staged release of steps | `onyx/coordinator.py`; ML Intent: `docs/intent.json` |
| ML sandbox | ML sandbox | the governed-versus-ungoverned run on the same scenarios; optional replays under a proposed rule or a failed model call, and a local-model run, none scored | `onyx/runs.py`, `onyx/eval.py`, `onyx/whatif.py`, `onyx/modeldown.py`, `onyx/localmodel.py`; `runs/ungoverned/`, `eval/results.md` |

Y.3172 clause 9, security of the pipeline: no provider key is in the source tree (a test greps every tracked file for the key pattern and fails on a hit); a run reads the KB and keys and writes its log only by appending chained events; the model adapter is the only outward call a run makes (`kb fetch` downloads sources outside a run). Tests: `tests/test_pipeline_security.py`.

## What we do not claim

- The answer keys are ours, written and hashed before the first live run (`onyx/data/keys/HASHES.txt`).
- The humans in the recorded runs (approvers, override attempts) are scripted steps, not people.
- UNVERIFIED rows in the manifest back no quoted clause; two of them record an absence (the PDPL Executive Regulations, the agentic framework text) that the register claims from the portal check written in the row, dated.
- No source on file shows how a UAE operator's assistant is governed; the Etisalat Virtual Assistant page lists what it does, not what stops it.

## Model

- Model: `claude-sonnet-5-5`, through Anthropic's OpenAI-compatible endpoint `https://api.anthropic.com/v1/`
  (`onyx/model.py`, one adapter for every model).
- Prices: https://platform.claude.com/docs/en/about-claude/pricing, read 2026-10-21 (`onyx/data/model_prices.json`).
- Bake-off: [`eval/bakeoff.md`](eval/bakeoff.md), one governed run per scenario (S1 to S5) per language per model.
- Scored run: [`eval/results.md`](eval/results.md), C5, Sonnet on prompt v5, two runs per scenario per language,
  governed (English / Arabic): action recall 0.96 / 1.00, citation validity 0.99 / 1.00, obligation proxy
  0.57 / 0.58; 2 of 112 key steps missed (pooled action recall 110 of 112 key steps, 95% interval 0.94 to 1.00).
- Ungoverned baseline: C3, Sonnet on prompt v3, three runs per scenario per mode per language.
- Local model: S2 recorded once on `qwen2.5:14b-instruct` through Ollama on a desktop GPU, same adapter, in
  `runs/demo-local/` and shown in [`docs/site/localmodel.html`](docs/site/localmodel.html); a demo of the adapter, not scored.

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
