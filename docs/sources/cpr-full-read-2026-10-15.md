# TDRA Consumer Protection Regulations v2.0: full read, Arabic check, gap verdicts

Read 2026-10-15 on Fable. Every article of the English text (1 to 30, 74 pages) was read in
full; the Arabic official text was extracted and compared clause by clause for every clause
the T1 build relies on. Replaces the "candidates to confirm" status of the seven gaps in
`domain-problem-scores-2026-10-14.md` and `gpt-stage1-choose-2026-10-14.md`.

## 1. Sources

| Item | Value |
|---|---|
| TDRA page listing the document | https://tdra.gov.ae/en/About/tdra-sectors/telecommunication/departments/regulatory-affairs-department/consumer-affairs (fetched 2026-10-15; lists "Consumer Protection Regulations, 25/07/2025, 1 MB") |
| English PDF | https://tdra.gov.ae/-/media/About/regulations-and-ruling/EN/CONSUMER-PROTECTION-REGULATIONS-VERSION-20-ISSUED-2572023.ashx |
| Arabic PDF | https://tdra.gov.ae/-/media/About/regulations-and-ruling/AR/CONSUMER-PROTECTION-REGULATIONS-VERSION-20-ISSUED-2572023-Ar.ashx (page title: لوائح أنظمة حماية المستهلك) |
| English file | 74 pages, cover "Version 2.0, Issued: 25 July 2023", PDF created 2023-07-28 (Word 2016). Copied to `standards-text/tdra-cpr-v2-en.pdf` and `.txt`. |
| Arabic file | 57 pages, same cover, PDF created 2023-07-28. Copied to `standards-text/tdra-cpr-v2-ar.pdf` and `.txt` (UTF-8). |
| Corpus copy | `corpus-text/pdf/3.2_TDRA_Consumer_Protection_Regulations_v2.txt`: 74 pages, 23,362 words against 23,372 in the official extraction, 435 "shall" in both. Same document. |
| Legal basis | CPR 1.1: Article 14(3) of Federal Law by Decree 3/2003 (Telecommunications Law). Binding on all UAE licensees (3.1). |
| In force | 30.1: one month after issue, so 2023-08-25; Articles 7 and 10 four months after, 2023-11-25. 30.2.1 repeals v1.5 of 2020-10-04. |
| Currency | The 25/07/2025 on the TDRA page is a listing date; the file it links is v2.0 of 2023. No v2.1 or v3.0 is listed on tdra.gov.ae (site search 2026-10-15). **v2.0 is the current text.** |
| Reported, not verified | e& and du licences renewed for 20 years from 2026-08-09; one trade report (tbreak.com) says the new licences carry "AI-readiness" obligations. The licence text was not found. Do not cite until read. |

**Annexes.** The contents page lists Annexe 1 (TDRA Consumer Dispute procedures), 2 (advertising
complaints), 3 (Compensation Scheme), 4 (exit charges), 5 (credit limits). None is in the
published PDF, English or Arabic, and a TDRA site search finds no separate file. For S5 use
the TDRA's service page instead: https://tdra.gov.ae/en/Services/dispute-resolution-with-service-providers
(the consumer must first complain to the provider; dispute lodged through UAE Pass; expected
time 5, 10 or 15 working days by complexity; free). One non-official guide (uaeexperthub.com)
claims a 2014 annex with 15 working days is still circulating; single source, unverified.

## 2. What the full read confirms, clause by clause

English verbatim is in the corpus text; Arabic verbatim is in `standards-text/tdra-cpr-v2-ar.txt`
(the extraction prints the "لا" ligature as "اال", e.g. "األغراض" = "الأغراض").

| Clause | English (short) | Arabic (short) | Verdict |
|---|---|---|---|
| 2.1.7 | Consumer Complaint: any correspondence or communication registered by any reasonable means at any place authorised by the Licensee, from a Subscriber expressing dissatisfaction or grievance | شكوى المستهلك: أي مراسلات أو اتصالات مسجلة عن طريق أي وسيلة ممكنة في أي مكان معتمد من قبل المرخص له ... يعبّر فيها عن عدم رضاه أو تظلمه | Same. Arabic "أي وسيلة ممكنة" (any possible means) is if anything broader. |
| 3.2.2 | Written information in Arabic or English as the Consumer prefers, both if unknown | تُكتب باللغة العربية أو الإنجليزية حسب تفضيل المستهلك ... بكلتا اللغتين | Same. The agent must work in both languages. |
| 3.3 | Transparency and fairness in all dealings; information complete, transparent, accurate, truthful | التصرف بشفافية في جميع التعاملات ... مستوفاة وتتسم بالشفافية والدقة والصحة | Same. |
| 4.3 | No service registered, charged or availed that the Subscriber has not expressly ordered | عدم تسجيل أو استيفاء رسوم ... من خدمة لم يطلبها المشترك ... صراحةً | Same. |
| 4.6 | Consent record kept; in a dispute the Licensee must prove consent; otherwise a rebuttable presumption of no consent | الاحتفاظ بسجل عن موافقة المشترك ... افتراضاً قابل للدحض | Same. |
| 4.7.1 | Opt-in, positive affirmative action taken freely | خيار الاشتراك ... التأكيد بالإيجاب ... بحرية | Same. |
| 4.7.2 | Written, spoken and electronic interaction all acceptable if storable under 3.9 | تُقبل جميع أشكال الموافقات الخطية منها والشفهية والتفاعل الإلكتروني | Same. |
| 4.7.3 | No consent by failing to opt out or to undo a pre-selected option | لا يعتبر المشترك أنه قد أعطى الموافقة لمجرد أنه لم يلغِ خيار الاشتراك | Same. |
| 4.10 | In all digital applications no single-click; multi-step; "unless objectively justified otherwise, or expressly specified otherwise", 2FA required | في جميع التطبيقات الرقمية ... "بنقرة واحدة" ... ما لم يتم التبرير موضوعياً بخلاف ذلك أو تحديد خلاف ذلك صراحةً ... المصادقة الثنائية | Same, same qualifier. |
| 4.11 | Default 2FA is OTP | كلمة المرور لمرة واحدة OTP | Same. |
| 4.17.3 | Telephone sale: voice recording of verbal consent | تسجيل صوتي يثبت موافقة المشترك الشفوية | Same. |
| 4.22.1 to 4.22.3 | Licensee App: no single click; accept terms; "no" is the default on yes/no screens | لا تتم عملية الشراء بمجرد نقرة واحدة ... تحديد الخيار "لا" بشكل افتراضي | Same. |
| 5.4.1 | PSCM: by the Licensee, written, SMS or agreed channel, right after purchase, with date, name, price, recurrence, cancel link | رسالة تأكيد ما بعد الاشتراك ... | Same. |
| 13.6 | On a cancellation request, act with immediate effect to suspend the service and charges | التصرف فوراً لتعليق الخدمة المعنية وما قد يتراكم عليها من رسوم | Same. |
| 17.2 | Notice at least twenty-eight (28) calendar days before a price increase, with set content and an opt-out route | إشعار ... بمدة لا تقل عن ثمان وعشرون يوماً | Same substance. **Arabic says "days", not "calendar days".** Quote the English when the distinction matters. |
| 22.1.1, 22.1.2 | Disconnection preceded "where-ever possible" by individual notice and warning (footnote 34: the Licensee must prove it was not possible); confined to the services concerned | مسبوقة، كلما أمكن ذلك، بإشعار فردي وتحذير ملائم ... قصر أي انقطاع على الخدمات المعنية | Same, footnote 34 present. |
| 22.2 | Warning content: actions to avoid disconnection, due dates, consequences, planned date and time | الإجراءات اللازمة ... تواريخ الاستحقاق ... التاريخ والوقت المخطط لهما | Same. |
| 22.3, 22.4 | Basic non-substitutable services kept; emergency numbers reachable during dunning | عدم تقييد ... الخدمات الأساسية ... الوصول بشكل مستمر إلى أرقام الطوارئ | Same. |
| 22.5 | Exception: a competent authority's official requests disconnection for public or national security | لا تنطبق أحكام المادة 22 في حال طلب مسؤول مفوض من جهة مختصة | Same. |
| 24.5 | Access to Subscriber Information limited to trained and authorised personnel (employees, directors, contractors, consultants) under a written agreement | تقييد الاطلاع على معلومات المشتركين ... موظفيهم المدربين والمفوضين | Same. |
| 24.6 + fn 35 | Prior consent before sharing with affiliates or third parties not directly involved; consent may be given in the contract if an opt-out exists | الحصول على موافقة مسبقة من المشترك قبل تبادل أي معلومات ... يجوز تقديم هذه الموافقة تعاقدياً ... شريطة وجود آلية ... أن يسحب تلك الموافقة | Same, footnote present. |
| 24.7, 24.8, 24.9 | Interconnection data never for marketing; no non-essential data about others; third parties directly involved bound by contract | Same | Same. |
| 24.10 | Disclose to the Subscriber free and without delay "after an adequate verification process" | بعد إجراء عملية تحقق كافية | Same, equally undefined. |
| 25.14 | Waive directory-enquiry charges when "an artificial intelligence assistance (AIA)" could not return the number | معالجة استفسار المستهلك بواسطة مساعد ذكاء اصطناعي (AIA) | Same. |
| 26.6 | "an adequate number of properly trained personal" (sic) to receive, process and respond to complaints | عدد كافٍ من الموظفين المدربين تدريباً مناسباً | Arabic confirms "personnel" (موظفين). |
| 26.7.1, 26.7.2 | 26.6 applies regardless of Mandatory Channel, and the provisions "preclude the use of non-human agents by Licensees in conversations with Consumers regarding Consumer Complaints" | تسري في كل الحالات بغض النظر عن القناة الإلزامية ... **يستثنى أو يستبعد منها** استخدام وكلاء غير بشريين من قبل المرخص لهم في المحادثات مع المستهلكين بشأن الشكاوى المقدمة من قبلهم | Same meaning. **Wording point:** the Arabic renders "preclude" as "يستثنى أو يستبعد منها" (is excepted or excluded from them). Read alone, "يستثنى منها" could be twisted to mean "exempt from 26.6"; "يستبعد" (excluded, ruled out) settles it in the sense of the English. Quote both languages in the report. Which language prevails is not stated in the CPR; not established. |
| 26.13.2, 26.13.3 | Reference number and indicative time-frame; immediately by phone or visit, within one business day if written | رقم مرجعي ... الإطار الزمني ... فوراً ... خلال يوم عمل واحد | Same. A chat is written (one business day); a voice bot is telephone (immediately). The governed agent does it immediately in both. |
| 26.14.2 | Conclude within twenty (20) business days | عشرين (20) يوم عمل | Same. |
| 26.16.1 | TDRA dispute: resolve and respond within three (3) business days | ثلاثة (3) أيام عمل | Same. |
| 28.11 | Advertisements aimed at children: no undue or exploitive pressure | الإعلانات الموجهة للأطفال | Same. |

**AI in the text.** The only clauses in either language that mention AI, automation or
non-human agents are 25.14 (AIA, directory enquiries) and 26.7.2 (non-human agents,
complaints). Confirmed by search of both full texts ("artificial", "automat", "non-human",
"bot", "machine"; "ذكاء اصطناعي", "بشري", "آلي", "روبوت"). "Automatically" appears only for
bundle renewal (2.1.16) and receipts (18.9). "Personnel" appears in 24.5 and 26.6.

## 3. The seven gaps: verdicts

Each verdict rests on the full read. "Kept" means no article covers it. Quote the clauses
named here when the gap goes in the report; judges push back on gaps (S2 25:23).

1. **No duty to tell a consumer they are talking to an AI. KEPT.** No clause says it. The
   closest hooks are 3.3 (transparency and fairness in all dealings; information complete,
   accurate, truthful) and 28.24 (advertisements must make clear who is legally responsible),
   neither of which names AI or disclosure of a non-human counterpart. The non-binding Ethics
   guideline 3.3.2.2 remains the only UAE text that says it.

2. **No rule on when an AI conversation becomes a complaint conversation, or a detection
   duty. NARROWED.** The trigger exists: 2.1.7 makes a communication a Consumer Complaint the
   moment a Subscriber expresses dissatisfaction or grievance through any reasonable means at
   any authorised place, and 26.4.5 names the Licensee App as such a place; 26.13.1 adds a duty
   to assist a Consumer to formulate and lodge a complaint; 26.13.2 and 26.13.3 fix the
   acknowledgement and its timing. What is missing, and stays a gap: (a) nothing says what an
   automated channel must do at that moment (stop, hand over, how fast); (b) 26.7.1 ties 26.6
   to the Mandatory Channels (26.4.1 to 26.4.4) while 26.7.2 is unqualified, so an operator could
   argue that an app chatbot (a non-mandatory channel, 26.4.5) sits outside 26.7; (c) the Arabic
   wording of 26.7.2 (section 2). Our governed design applies 26.7.2 to every channel, the safe
   reading, and reports the ambiguity as the gap.

3. **"25.14 is the only AI clause." CORRECTED.** Two clauses, not one: 25.14 (AIA, directory
   enquiries only) and 26.7.2 (non-human agents, complaints only). Neither sets any standard for
   AI conduct in sales, service changes, data handling or disconnection. State it that way.

4. **Automated disconnection or credit decisions governed only by PDPL 18. RESTATED.** The CPR
   does govern the act, whoever decides it: 22.1.1 notice and warning, 22.2 content, 22.1.2
   confinement, 22.3 and 22.4 basic and emergency services, 8.8.2 notices at 80, 95 and 100
   percent of the credit limit, 8.11.4 final warning, 8.9.1 interruption only if the information
   and consent duties were met, footnote 34 putting the burden of proof on the Licensee. What the
   CPR lacks is any right to human review of the decision itself. PDPL 18(1) gives a right to
   object to automated decisions with legal or serious effects; 18(2) removes that right where
   the automated processing is in the contract terms, required by other legislation, or
   consented to under Art 6; 18(4) separately says "The Controller shall engage human resources
   in reviewing Automated Processing decisions, at the request of the Data Subject". My reading
   (inferred): 18(4) stands even where 18(2) applies, since it is not conditioned on 18(1). So
   the gap is: the CPR is silent on human review of automated disconnection; the PDPL supplies
   review on request but lets a contract term remove the right to object. 21(2)(a) requires an
   impact assessment before such processing.

5. **"Adequate verification process" (24.10) undefined for AI channels. KEPT, STRENGTHENED.**
   The CPR never defines identity verification anywhere: 4.15.2, 4.17.1 and 20.10.2 say "verify
   the identity"; 20.11.1 says "by asking the relevant security questions, or by following such
   other procedures used by the Licensee"; 10.7.1 "all relevant procedures". 2.1.35 defines 2FA
   and 2.1.15 OTP, but only for purchase consent, not for disclosure of Subscriber Information.
   So a voice or chat agent disclosing account data after "security questions" is within the
   letter of the CPR; the exposure to voice cloning and social engineering is covered only by the
   non-binding Deepfake Guide 2021 (inferred link, not stated in any text).

6. **Cabinet agentic-AI framework (2026-05-18) covers federal entities, not licensees; text
   unpublished. NOT CHECKED in this session.** Not a CPR matter. Stays as recorded.

7. **Spoken consent acceptable (4.7.2); no rule on consent elicited by an AI. KEPT, with a
   sharper form.** The CPR's consent conditions are organised by sales medium: business centre
   (4.15), telephone call to or from a call centre (4.17: identity, verbal pre-contract
   information, recorded verbal consent, PSCM, no 2FA), SMS or USSD (4.19), TV remote (4.20),
   Licensee App (4.22: no single click, accept terms, "no" default, PSCM, no express 2FA), online
   or other device (4.23: 2FA for each purchase). A conversational agent is not named in any of
   them. A voice agent reads naturally as 4.17 (no 2FA needed); a chat agent in the app as 4.22
   (no express 2FA) or as 4.10 (2FA "unless expressly specified otherwise"). Which sub-article
   governs decides whether an OTP is required at all. The build takes the strict reading (4.10
   plus OTP, 4.11) and reports the classification question as the gap.

**New candidate, from the full read (8). Subscriber Information sent to an AI model
provider.** 24.5 limits access to trained and authorised personnel under a written agreement;
24.9 lets data go to third parties "directly involved in the supply of the telecommunications
services" under a contract that makes them responsible; 24.6 bars sharing with third parties
not directly involved. A hosted LLM API that receives account data is none of these by name.
The PDPL's processor rules apply (not checked here). For the build: the care agent sends the
model the minimum, de-identified where possible, and the gate logs what left. Report it as a
design rule and a question for the regulator, not as a confirmed gap, until the PDPL processor
articles are read.

## 4. Findings that change or sharpen the build

- **Channel classification gate (gap 7):** the policy adviser must first classify the
  conversation (voice: 4.17; app chat: 4.22 and 4.10; web: 4.23) and apply that sub-article's
  conditions. Log the classification.
- **Renewal exception (4.4):** extending or renewing an expressly ordered service on terms
  consistent with the contract, or unquestionably without prejudice or to the Subscriber's
  advantage, needs no new consent. The ungoverned agent will abuse it ("this is just a
  renewal"); the gate must test the three conditions, not the label. Same for migration (4.9).
- **"No" is the default (4.22.3, 4.23.3):** any yes/no the agent offers on screen defaults to no.
- **Partner services (9.4.2):** the cap is AED 0 per month by default; the agent cannot sell a
  partner add-on unless the Subscriber has set a cap (9.4.3). Out-of-bundle data needs a recorded
  opt-in (16.9.2).
- **Contractual consent to sharing (24.6, fn 35):** the sharing gate must check for a recorded
  consent, contractual or later, and that no opt-out was exercised, not just "no consent in the
  chat".
- **Cancellation (13.4, 13.6, 13.8):** cancelling must be as easy as ordering; on a request the
  agent suspends the service and charges immediately; no exit interview without consent and only
  after cancellation. A retention pitch that delays the cancellation breaches 13.6. Good unseen
  event.
- **Language (3.2.2):** written information in the Subscriber's preferred language, both if
  unknown. Ties to Readiness dimension 6.
- **Accuracy (3.3, 5.3):** every price or term the agent states must match the tariff. A
  hallucinated price is a breach, not just an error. Gate: quoted figures must come from the KB.
- **Marketing (28.25, 28.26):** no intrusive or coercive advertising; a Consumer's request not to
  be contacted, at certain times or at all, must be honoured. Pair with 3.11 and PDPL 17.
- **Burden of proof (4.6, 4.24, 9.6, 20.4, fn 34):** in every dispute the Licensee must produce
  the evidence; without it the presumption runs against it and the TDRA may order a refund (4.25.4,
  9.6). This is the strongest argument for the audit log: it is the evidence the regulation demands.
- **Disconnection exception (22.5):** a competent authority's security request bypasses Article
  22. The TDRA agent or a security-authority event is a legitimate unseen scenario.
- **Records (3.9):** consent and 2FA records five years, recordings two, complaints two, PSCMs
  and notices two. The KB's audit fields should carry a retention class.

## 5. Not read or not covered

- The Telecommunications Law (Federal Law by Decree 3/2003) and the licence conditions, including
  the 2026-08-09 renewals and their reported AI obligations.
- The five annexes (not published in the PDF; not found on the site).
- CPR v1.5 (2020) and any TDRA guideline, directive or Temporary Instruction issued under 3.14
  or 3.8 since 2023; the TDRA QoS framework.
- The Arabic text beyond the clauses compared in section 2 (57 pages extracted; not read whole).
- PDPL processor articles (for candidate gap 8); PDPL Art 6 consent conditions.
- Which language prevails if the English and Arabic texts differ: not stated in the CPR.
