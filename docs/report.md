# AI for Good Sandbox Hackathon – Onyx – Mizan

**Team leader:** Iyas Shraim (BAU Faculty of AI)
**Team members:** Mohammed Rawashdeh, Yanal Faouri, Zaid Saaydeh
**Contact details:** iyas.shraim@gmail.com, +962 790 602 577
**GitHub link:** https://github.com/SHRA1M/onyx-hackathon-build (public from 2026-11-09)

## Introduction

Mizan is a consumer-care AI for a synthetic UAE operator, built around three choices. The case is a subscriber in a
chat or on a call, not an institution in a drill. The model proposes and plain code written from the binding UAE
texts decides: every allow, hold or block names the clause it relied on, its page and its words, in English and
Arabic. It is scored in both languages, because the texts are published in both. Every step goes to a hash-chained log that a judge can replay offline without an API key, and replay again under a proposed rule: a what-if question for the policymaker.

The first contact at a UAE operator is already an AI, and e& reported 371,476 customer complaints in its UAE
operations for 2025 (e&, Sustainability Report Appendices 2025, Appendix 1). The binding texts already bar such an
AI from charging without an express order (Consumer Protection Regulations v2.0, CPR 4.3), sharing subscriber data
without consent (24.6), disconnecting without warning (22.1) and handling a complaint: CPR 26.7.2 requires licensees
to "preclude the use of non-human agents by Licensees in conversations with Consumers regarding Consumer
Complaints".

The knowledge base holds 74 documents: the Telecommunications Law 3/2003, the
CPR v2.0, Licence 2/2026, the Personal Data Protection Law 45/2021 (PDPL) and twenty-seven other UAE laws, resolutions and
TDRA instruments; ITU-T Y.3172, Y.3173 and the AI Readiness Report 2.0; and
twenty-one foreign texts used only as global examples. 69 are verified: the issuing body's file is on disk with its SHA-256, and a test on every push checks each
clause the gates cite word for word against it; two unpublished texts and one unreachable one back no claim. No consumer data was used.

## Description of the use case

**The problem and the existing protections.** The four acts above each have a binding rule written for a sales call, a shop or an IVR; nothing tells a conversational agent where its mandate ends, and nothing
records, in a form a regulator can check, which clause each act relied on.

**Our solution.** Five agents with bounded mandates (care, the policy and legal adviser, the Data Office, TDRA and a coordinator). The model proposes a verb with clause
ids and a verbatim quote. Plain-code gates return allow, hold (a named human must act
first), block, or insufficient evidence (the agent abstains; a candidate gap is logged). The cases the texts reserve
for a person go to a person: a Consumer Complaint (CPR 26.7.2, licence 9.1), a contested automated decision
(PDPL 18(4)), and every hold; no human approves every answer, because the texts do not ask for it. `eval` recomputes every figure in this report from the logs.

**What is different.** The same five scenarios run governed and ungoverned on the same model: ungoverned, 2.3 (English) and 2.1 (Arabic) proposals per run passed that the gates reject
`[C3, prompt v3, three runs per scenario per language]`.

## Use case requirement

One requirement per Y.3172 node, each implemented and tested unless marked. **SRC-1** injects carry facts, never answers; **SRC-2** 74 documents with URL, SHA-256 and status,
chunked by clause. **C-1** each agent sees only the steps released to it. **PP-1** retrieval is scoped to the
agent's mandate; a cited id outside the clauses given is invalid. **M-1** one model behind an OpenAI-compatible
adapter. **P-1** gates for the personal data rules and the complaint bar; **P-2** four verdicts, one block without
override. **D-1** hand-over to a named human and the gates' deadlines; **D-2**, not built: routing for a step the
scenario did not name. **SINK-1** log, gap register, replay pages. **MLFO-1** every log records the model, prompt,
gate version and key hashes. **SB-1** selftest and the full suite run in CI on every push.

## Mapping with ITU-T Y.3172, Readiness 2.0 Report, and domain-specific policies

| Node | Mizan (requirement) | Readiness 2.0 dimension or factor; its metric; evidence in the running system | Documents |
|---|---|---|---|
| SRC | injects; manifest with URL, hash, status, language (SRC-1, SRC-2) | 11 AI for Inclusion, "support for regional languages": every clause in Arabic where published; Arabic runs scored | CPR v2.0 EN and AR; Telecom Law 3/2003 |
| C | per-agent inbox, staged release (C-1) | 7 Strategy Alignment, "coordination between service providers": operator, regulator and Data Office as separate agents (S5) | Licence 2/2026 (9.1, 9.2.4); PDPL |
| PP | clause chunks; mandate-scoped retrieval (PP-1) | 10 AI & Policies, "policies for nodes in AI pipelines": the policy text is the retrieval unit | all KB rows; `kb/export/` |
| M | one adapter, any OpenAI-compatible model (M-1) | 6 Human Interface, "AI models in the local language": drafts in both; the gate between draft and subscriber | PDPL 7(5), 8(1), 13(2), 22, 23; licence 3.4.1 |
| P | plain-code gates; four verdicts (P-1, P-2) | 8 Collaboration with AI, baseline "only AI with no human-in-the-loop": the governed-against-ungoverned run | CPR 4.3, 4.10, 4.11, 22.1, 24.6, 24.10, 26.7.2; Cabinet 56/2024; PDPL 18(4) |
| D | hand-over; deadlines; routing not built (D-1, D-2) | 6 Human Interface: hand-over with both quotes; no Y.3172 node outcome for it (gap 8) | CPR 26.13.2, 26.13.3; QoS v3.0 T1(2a) |
| SINK | log; replay; gap register (SINK-1) | 10 AI & Policies, "policy inputs from case briefs": the gap register is an output | Y.3172; Readiness 2.0; IMDA, EU AI Act, GDPR, COPPA |
| MLFO | staged release; model, prompt, gate version and key hashes per run (MLFO-1) | Standards factor: configuration recorded and replayable | Y.3172 |
| ML sandbox | selftest and suite in CI; the governed-against-ungoverned pair (SB-1) | Sandbox factor: same scenarios with and without gates, same model | Y.3172; Readiness 2.0 |

Five dimensions are claimed with running-system evidence (6, 7, 8, 10, 11); 1 and 13 by documents only; the other
six are not claimed.

![Figure 1](docs/fig/fig1-architecture.png)

*Figure 1. Mizan on the Y.3172 nodes; the model proposes, the P node decides, D hands a complaint to a person.*

## Error scenarios

**S1, roaming before a flight.** App chat classified (CPR 4.22, 4.10, 4.11). Roaming costs after verification
(24.10): allow. A bundle offered: hold until the OTP and the consent form, then allow (P-1). Whether CPR 4.4 covers
an expired bundle's renewal is not written: candidate gap.

**S2, a billing question becomes a complaint.** Care removes a charge with no consent record (4.3): allow. "I never
ordered this, I am fed up": a Consumer Complaint (2.1.7). Care drafts a reply; the gate blocks it under 26.7.2 and
licence 9.1, and the coordinator hands the conversation to a named human (D-1). How fast must a chat hand over? No
text: gap 1. Replayed as a what-if under the rule the register recommends, the held step releases, the hand-over duty gains its
clock, and a new finding appears: the hand-over time must be recorded (`docs/replay/whatif-S2-gap-1.md`). With the model call made to fail at step 3, the coordinator's deny-by-default hold hands the conversation to the same human, with no model in that step (`docs/replay/model-down-S2.md`).

**S3, a partner wants the data, and the model provider is abroad.** A partner asks for interconnection data: block
(24.6). An override to send identifiers to the provider abroad: block, no override (P-2; PDPL 22, 23(2); gap 5). A de-identified payload under
the processor contract: allow. A retention offer to a Do Not Call number: block (Cabinet 56/2024).

**S4, non-payment and an automated disconnection.** Disconnection with no warning on file: block (22.1). Notice
given, warning limited to the unpaid service: allow. The subscriber contests the automated decision; the Data Office
requests a human review (PDPL 18(4)): allow. By when, and who hears a refusal? Not written: gap 4.

**S5, a TDRA dispute and a loss report.** A lost device reported over voice: hold until identity is verified
(24.10; Decision 16/2026). What "adequate verification" is on a remote channel: gap 3. The human verifies, the block
proceeds: allow; TDRA requests the report.

**Results**, two runs per scenario per language, means over S1 to S5, English / Arabic `[C5, governed, two runs per
scenario per language, mean over S1 to S5, en / ar]`: citation validity 0.99 / 1.00 (one id, S2 English); action recall
against the frozen keys 0.96 / 1.00 (110 of 112 key steps; both misses English, S3-4 and S4-4), 95% interval 0.937 to 0.995 pooled; abstention on the one
unanswerable step per scenario 1.00; expected gaps: 5 of 7 found in every run, 2 missed (both in S1), 3 unexpected register ids flagged. The gate decides in a median of 0.46 ms; the model's proposal
takes a median of 7.8 s `[C3, governed, 222 decisions, 156 calls]`.

![Figure 2](docs/fig/fig2-results.png)

*Figure 2. (a) C5, two runs per scenario per language: action recall and citation validity. (b) C3, three runs per
scenario per language: gate rejection governed, and claims allowed ungoverned.*

## Policy gaps and standards gaps derived from the mapping exercise

Found by absence: for each gap the register lists the documents and clauses searched, in both
languages, before the gap was claimed.

| # | Gap | Kind | Addressee | Global example |
|---|---|---|---|---|
| 1 | Complaint hand-over: the bar and the human are sourced (CPR 2.1.7, 26.7.2, licence 9.1) and the complaint has clocks (26.13.3, 26.14.2); the transfer has none: what the agent does when the conversation turns, when the human is in it; du's code names a chatbot channel and sets no hand-over rule | standards | TDRA | Spain Ley 10/2025 Art 8(2), 8(3) |
| 2 | Consent elicited by an AI: the CPR accepts stored spoken consent (4.7.2) and sets the OTP need by sales medium (4.10, 4.17, 4.22), naming no AI channel; the PDPL exempts what the contract needs (4(9)) and wants any further data use consented in writing or electronically (6(1)(b)), so a spoken "yes" buys the service | coordination | TDRA, UAE Data Office | CRD 2011/83 Art 8(2); IMDA 2.2.2; Singapore ETA s. 15 |
| 3 | "Adequate verification process" (CPR 24.10) undefined for a remote channel; Electronic Transactions Art 33 trust levels never mapped to it | standards | TDRA | eIDAS Art 8(1), 8(3)(c) |
| 4 | Automated disconnection: the PDPL 18(4) human review has no procedure or deadline, and the complaint route to the Data Office (Art 24) has no clock either | responsibilities | UAE Data Office | GDPR Art 22(3), 12(3) |
| 5 | Subscriber data to a hosted model provider: the duties exist (PDPL 7(5), 8(1), 13(2), 23(1)(a), licence 3.4.1), the machinery (Art 22 list, 23(2), 8(11)) has not been issued | legislative | UAE Data Office | GDPR Art 28(3)(a), 45(1) |
| 6 | AI disclosure: no general duty to tell a consumer they are talking to an AI; Electronic Transactions 11(2) asks only that the person "knows, or is supposed to know" the system contracts automatically | legislative | Cabinet | EU AI Act Art 50(1), 50(5) |
| 11 | A misheard order: the CPR defaults an on-screen answer to "no" to avoid an accidental "yes" (4.22.3, 4.23.3) and wants an OTP per purchase (4.23.2); nothing says what a voice or chat channel must do when it interprets the words itself | standards | TDRA | US TSR 16 CFR 310.3(a)(3)(ii) |
| 12 | Agent authority: Mizan's stop at S2-3 sits at Y.3173 'Human and System' on the decision step (Table 7-1) and its hand-over is Readiness D9's inference-to-action latency in the other direction; mapped there, neither text measures when an acting agent must stop, how often it hands over or how long that takes (Table 7-2 NOTE 1 gives a human's order the highest authority; it never requires the system to ask). Left open at ITU's request (2026-10-30). | standards | ITU | EU Roaming Reg 2022/612 Art 14(4); EU AI Act Art 14(4)(e) (high-risk, from 2027) |
| 8 | Y.3172 has no node outcome for a hand-over to a human: every node outcome is the output moving on to a sink that acts | standards | ITU-T | 3GPP TS 28.535 §4.2.3; ETSI ZSM 009-1 §7.2.2.4 |
| 9 | A child on the line: the caregiver signs the terms (Child Digital Safety Law 26/2025, 11(1)(b)) and under-13 data needs verified caregiver consent (7(1)); the Art 11 instructions and Art 16 penalties are unpublished, and Resolution 106/2026's age checks reach social media only (Art 2); nothing says how a telecom channel learns the person is a child | legislative | TDRA, Cabinet | US COPPA Rule, 16 CFR 312.5(a)(1), (b)(1) |
| 10 | Arabic on an automated channel: the language is set and its omission fined (CPR 3.2.2, Consumer Law 26, Cabinet 66/2023 Annex 2); no text requires the Arabic answer to be as good as the English one, and the QoS Policy has no indicator per language | standards | TDRA | Wales WLS Regs 2015 Sch 1 Std 15, 22 |

Recommendations. TDRA: a stated time and action when a chat becomes a Consumer Complaint, measured like T1(2a) (1);
the AI agent placed among the Article 4 sales media (2); the Article 33 trust level 24.10 requires (3); a read-back of the
understood order before the OTP on voice and chat channels (11); the Art 11 instructions with a caregiver check (9); QoS indicators per language, Arabic and English reported separately with a parity band (10). The UAE Data
Office: the 18(4) procedure (4); the processor terms, transfer controls and country list (5); whether spoken consent
meets 6(1)(b) (2). The Cabinet: AI disclosure at first contact (6). ITU-T: a policy-node outcome that routes the
case to a named human (8). Gap 10 is measurable: action recall 0.96 English, 1.00 Arabic (C5) is the indicator the QoS Policy lacks.

## Limits and next steps

The answer keys are ours, hashed before the first run; the humans in the recorded runs are scripted, and no run
records an approval. Before the final: the seven unseen scenarios run cold, no keys; routing (D-2); a team member approves holds; a data-protection practitioner reads the gates' law. ITU can reuse the Arabic chunks and runs, the manifest and the agent manifests (SNAI).
