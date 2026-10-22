# Telecom Law, the 2026 licences and every other UAE rule that binds an operator's AI care agent

Read 2026-10-16 and 2026-10-17 on Fable. Iyas's brief: read the Telecommunications Law
(Federal Law by Decree 3/2003) and the e& and du licence conditions renewed 2026-08-09 in full,
search for every other UAE rule that binds a telecom operator's AI care agent, Arabic sources
beside English, then re-check the eight gaps of `cpr-full-read-2026-10-15.md`: kept, narrowed
or killed, with the clause. Three Fable research agents swept data and cyber law, consumer and
contract and AI instruments, and the TDRA's instruments since 2023; their notes are in
`research-notes/uae-rules-2026-10-17/`. Everything quoted below was read from the primary text
unless marked otherwise. Inferences are marked.

## 1. Sources read in full by me

| Instrument | What was read | File in `standards-text/` |
|---|---|---|
| Federal Law by Decree No. 3 of 2003 Regulating the Telecommunications Sector, as amended by 1/2005, 5/2008 and Federal Decree-Law 23/2020 | English in full, twice: the official legislation portal's consolidated text (uaelegislation.gov.ae/en/legislations/1132, "last update listed 27 Sep 2020", "Legislation Amendments: 3", state Active; PDF created 2024-10-03, 34 pages) and the TRA's own 2008 edition (WIPO Lex copy, 40 pages, with endnotes on every retranslated word). Arabic: the portal's consolidated PDF (27 pages, created 2025-06-09) for Articles 13, 14, 72 to 79 bis, read from page images. | `telecom-law-3-2003-consolidated-2020-portal-en.pdf/.txt`, `-ar.pdf/.txt`; `telecom-law-3-2003-tra-edition-2008-en.pdf/.txt`, `-ar.pdf`; the TDRA's 2022 print edition EN and AR (`-tdra-edition-2022-*-imageonly.pdf`, no text layer; its cover notes "Renamed to TDRA based on Article 1 of Federal Decree No. (23) of 2020") |
| Public Telecommunications Licence No. 2/2026 to Emirates Telecommunications Group Company PJSC (e&) | In full, 47 pages, bilingual (English left, Arabic right, in one document). Issued by the TDRA Director General 2026-08-06; term 2026-08-09 to 2046-08-08. | `licence-2-2026-etisalat-public-telecom-en-ar.pdf/.txt` (source: https://tdra.gov.ae/-/media/About/LICENSING/EN/Licence-22026-Etisalat-Public.ashx, fetched 2026-10-16) |
| Public Telecommunications Licence No. 3/2026 to Emirates Integrated Telecommunications Company PJSC (du) | Diffed line by line against 2/2026: identical apart from the licence number, the licensee's name, Article 16.6 (replaces Licence 2/2006 instead of 1/2006) and line breaks. | `licence-3-2026-eitc-du-public-telecom-en-ar.pdf/.txt` (https://tdra.gov.ae/-/media/About/LICENSING/EN/Licence-32026-EITC-Public.ashx) |
| Federal Decree-Law No. 26 of 2025 Regarding Child Digital Safety | English in full (16 pages); Arabic for Article 11. Issued 2025-10-01, in force 2026-01-01 (Art 20), one year to regularise (Art 18). Listed by the legislation portal as related to the Telecom Law. | `child-digital-safety-law-26-2025-en.pdf/.txt`, `-ar.pdf/.txt` |
| Cabinet Resolution No. 106 of 2026 Regulating Children's Access to Social Media Platforms | Arabic in full (7 pages, issued 2026-06-17, in force the day after Gazette publication). English download refused by the portal (Cloudflare) on 2026-10-16. | `cabinet-resolution-106-2026-children-social-media-ar.pdf` |
| Supreme Committee Resolution No. 3 of 2004 issuing the Executive Order of the Telecom Law | Only the cover page is published on tdra.gov.ae (Article One heading and Article 75 on publication, signed 2004-12-28). The 75 articles themselves are not in the file. Not read. | `executive-order-resolution-3-2004-cover-only-en.pdf` |

Where the TDRA site lists the law: https://tdra.gov.ae/en/Pages/legal-references (fetched 2026-10-16). Where it
lists the licences: https://tdra.gov.ae/en/About/tdra-sectors/telecommunication/departments/regulatory-affairs-department/licensing
("Public Telecom: Etisalat, View License; Du, View License"; the Documents tab still lists the 2006 licences
dated 01/01/2006). The Arabic licensing page links the same two PDFs, so there is no separate Arabic licence file;
the Arabic text sits inside each PDF and Article 16.7 makes it the binding version.

**The renewal, from the press (not official text):** seven outlets on 2026-08-12 and 2026-08-13 (Emarat Al Youm,
Al Khaleej, Al Bayan, Argaam, Arabian Business, tbreak, Telecom Review) report the TDRA Board renewed both public
licences for twenty years from 2026-08-09 to 2046-08-08, replacing the 2006 licences, "in accordance with the
amended Federal Decree-Law regulating the telecommunications sector", with strengthened requirements on network
resilience, backup capacity, international connectivity, quality of service, national roaming and subscriber
protection. The TDRA's own press release was not fetched by me (agent notes may have it). **The "AI-readiness
obligations" that one trade report attached to the renewal are not in the licence text: see section 3.**

## 2. The Telecommunications Law: what in it binds the care agent

The law regulates the operator, not the channel. It never mentions automation, software agents,
artificial intelligence, consent or identity verification. Its weight for us is in four places: the
TDRA's power to make the rules the agent must obey (Art 14), the licence as the instrument that carries
them (Art 32), the offences a careless agent could commit for its employer (Art 72), and the fines
(Art 79 bis). Arabic prevails: the portal says so on every page and the TRA's 2008 edition prints it on
its cover ("THE ARABIC VERSION OF THIS LAW SHALL PREVAIL IN CASE OF ANY DISCREPANCY").

| Article | English (portal translation, verbatim) | Arabic (portal, verbatim) | Why it matters to the agent |
|---|---|---|---|
| 1, "Regulated Activities" | "Operating a public telecommunications network and providing telecommunication services to subscribers in addition to any other activities the High Committee specifies in accordance with this Decree-Law." | not compared | The care agent is part of "providing telecommunication services to subscribers", so it sits inside the licensed activity, not beside it. Inferred. |
| 13(2), 13(3) | "Ensure that the telecommunications sector provides high quality and efficient services to subscribers"; "Ensure that Licensees comply with performance quality standards and satisfy the terms of their licenses" | "الارتقاء بمستوى الخدمة التي يقدمها قطاع الاتصالات بما يحقق صالح المشتركين"; "تقيد المرخص لهم بمعايير الجودة في الأداء والالتزام بالشروط المحددة في التراخيص الممنوحة لهم" | The TDRA's statutory objectives; the base for every quality and consumer rule. |
| 14(3) | "Terms and standards of services provided to subscribers by Licensees including, quality assurance standards for services and terms regarding the provision of services and the resolution of subscribers' complaints and disputes, subscriber information access, use of information by subscribers and subscriber billing." | "شروط ومستوى ونطاق الخدمات التي يقدمها المرخص لهم للمشتركين والخدمات الشمولية والخدمات الطارئة، بما في ذلك معايير جودة الخدمات المقدمة وشروط تقديم الخدمات والفصل في شكاوى المشتركين والنزاعات وتزويد المشتركين بالمعلومات واستخدام المعلومات الخاصة بالمشتركين وتزويدهم بالفواتير." | **The root of the CPR (CPR 1.1 cites it) and of any future AI-channel rule.** The Arabic says "the use of the information pertaining to subscribers" (استخدام المعلومات الخاصة بالمشتركين); the portal's English "use of information by subscribers" is a mistranslation, and the TRA's 2008 edition ("usage of subscriber personal information") is the faithful one. Quote the Arabic. So the TDRA already has express power to regulate how an operator's systems use subscriber data, handle complaints and inform subscribers; nothing in the law stops it from writing an AI-channel rule tomorrow. |
| 14(8) | "Terms for providing, setting up and operating directory assistance." | "شروط توفير وإعداد وتزويد خدمات الاستعلامات والدليل." | The hook for CPR 25.14 (the AIA directory clause). |
| 14(13) to 14(21) | Added 2020: digital government strategies, standards and platforms, "the provision of an exceptional and seamless customer experience" (14(20), 14(21)) | items 15 to 23 in the Arabic numbering of the portal PDF | Government digital services only. They do not reach a private licensee's channel. Note the numbering differs between the English (21 items) and Arabic (23 items) portal texts; cite by content. |
| 30 | "Licensees shall accommodate special needs and requirements by contributing to the provision of such telecommunications services and equipment and ensure non-discrimination when providing the same." | not compared | A statutory non-discrimination duty on the operator; relevant to Readiness dimension 6 and to an agent that treats Arabic and English callers differently. |
| 32 | "The High Committee shall determine the form and content of licenses issued in accordance with this Decree-Law. Licenses are required to contain information on the duration of their validity and any mandatory terms designated by the High Committee." | not compared | The licence conditions are law-backed, not a contract. ("High Committee" became "the Board" under 5/2008; the portal translation keeps the old word.) |
| 72(2) | "Illegally copies, discloses, or distributes the content of a telephone call or text message or any of the telecommunications services – whether he was an employee of a licensee or affiliated with it in a manner that enables him to have exposure to the content of a telephone call or text message or any of the telecommunications services." Imprisonment up to one year and/or AED 50,000 to 1,000,000. | "كل من نسخ أو أفشى أو وزع بدون وجه حق فحوى أي اتصال أو رسالة هاتفية أو أي من خدمات الاتصالات سواء كان عاملاً لدى أي مرخص له أو مرتبطاً معه بأية علاقة تتيح له الاطلاع على فحوى أي اتصال أو رسالة هاتفية أو أي من خدمات الاتصالات." | The confidentiality offence. It covers the content of communications and "any of the telecommunications services", and it reaches anyone "connected to [the licensee] by any relationship that allows access" (مرتبطاً معه بأية علاقة), which on its face includes a contractor or a hosted model provider given call or chat content. Inferred: a care agent that reads a subscriber's message history to a third party is within this article. |
| 72 bis (4) | "Whoever uses forgery or fraud with the aim of obtaining telecommunications services, subscribing to it, or providing it to others, shall be punished with imprisonment and a fine that does not exceed AED (1,000,000) ... It shall be considered an aggravated instance if any of the preceding acts were performed with the aim of committing a crime." | "يعاقب بالسجن وبالغرامة التي لا تزيد على (1.000.000) مليون درهم أو بإحدى هاتين العقوبتين كل من قام بالتزوير أو بالاحتيال بهدف الحصول على أي من خدمات الاتصالات أو الاشتراك بها أو توفيرها للغير. ويعتبر ظرفاً مشدداً القيام بأي من الأفعال السابقة بهدف ارتكاب جريمة." | The social-engineering attacker's offence (gap 5). It punishes the impostor; it puts no verification duty on the operator. |
| 72 bis (5) | "Whoever provides a third party with any of the telecommunications services without obtaining the documents determined by the implementing regulations" : imprisonment and/or AED 50,000 to 1,000,000. | "كل من قام بتزويد الغير بأي من خدمات الاتصالات دون الحصول على الوثائق التي تحددها اللائحة التنفيذية لهذا القانون" | The documents rule behind SIM registration. An agent that activates a service without the required documents exposes the operator. The Executive Order that lists the documents is not published (section 1). |
| 75 | "After obtaining prior approval from the Authority, a Licensee may place under surveillance any equipment or other thing which he reasonably suspects of being used in a manner contrary to Article (72)". | "يجوز للمرخص له بعد الحصول على إذن مسبق من الهيئة أن يضع تحت المراقبة أي جهاز أو خلافه إذا توافرت لديه أسباب مقبولة للاعتقاد بأنه يستغل في أي مخالفة منصوص عليها في المادة (72)" | Surveillance of a suspected fraud line needs TDRA approval first; a fraud-detection agent cannot do it alone. |
| 77 | "Crimes committed by corporate entities will be subject to the corresponding penalty provision applicable to the crime under this part of the Decree-Law." | "إذا ارتكبت إحدى الجرائم المنصوص عليها في هذا الباب من قِبل أي شخص اعتباري تطبق عندئذٍ على ذلك الشخص الاعتباري عقوبة الغرامة المقررة لتلك الجريمة في هذا الباب." | The operator, as a juridical person, pays the fine for its agent's act. |
| 79 bis (1) | "Whoever violates any provision of this Law's provisions or its implementing regulations, or any regulations, resolutions, instructions, or rules issued pursuant to it, shall be punished with a fine that is not less than AED (50,000) ... and does not exceed AED (200,000)". | "يعاقب بالغرامة التي لا تقل عن (50.000) خمسون ألف درهم ولا تجاوز (200.000) مائتي ألف درهم كل من خالف أي حكم آخر من أحكام القانون أو لائحته التنفيذية أو الأنظمة أو القرارات أو التعليمات أو القواعد الصادرة بموجبهما." | A CPR breach is a breach of "regulations ... issued pursuant to" the law. The same range reappears in licence Article 16.3.2. |
| 79 bis (2) | "The Board of Directors may impose administrative fines on licensees in the event of their violation of the provisions of the law, its implementing regulations, decisions, regulations, policies or instructions issued by the Board of Directors or the Authority. The Cabinet shall issue a resolution on the schedule of violations and fines imposed on licensees provided they do not exceed (10,000,000) ten million dirhams for each violation." | "لمجلس الإدارة توقيع غرامات إدارية بحق المرخص لهم في حال مخالفتهم أحكام القانون أو لائحته التنفيذية أو القرارات أو الأنظمة أو السياسات أو التعليمات الصادرة عن مجلس الإدارة أو الهيئة." (first paragraph; the ten-million cap is in the second) | The administrative route and its ceiling. **The Cabinet schedule it promises was not found** on the legislation portal or by search in either language on 2026-10-16; the only telecom fine schedules found are the 2024 telemarketing ones (section 4). |

Articles not quoted: 2 to 12 and 15 to 29 (the Authority's structure and finances, Etisalat's restructuring),
31 to 71 (licensing procedure, interconnection, equipment approval, numbering, spectrum, land, transitional
provisions), 73, 74, 76, 78, 79, 80 to 84. None binds a customer-facing channel. Article 14(5) ("Importing,
manufacturing, using and operating telecommunications equipment") and 42 (equipment approval) do not reach
software.

**Amendment check.** The portal lists three amendments (2005, 2008, 2020). The 2020 one (Federal Decree-Law 23/2020,
per the TDRA edition's cover note) renamed the Authority and added the digital-government items to Article 14; the
articles quoted above are otherwise the 2008 text. The portal's own English keeps "High Committee" where the 2008
amendment substituted "the Board"; the Arabic and the TRA edition use the Board. No amendment after 2020-09-27 is
listed as of the portal's update of 2026-10-16.

## 3. The 2026 licences: full read

Form: 16 Articles, 47 pages, English and Arabic side by side; Arabic binding (16.7). Signed by the Director
General on 2026-08-06, effective 2026-08-09. Article 2.1.3 is marked "[CONFIDENTIAL]" in both languages and is
the only redacted clause. The two licences are the same text.

**What is not in it.** The words "artificial", "automat", "AI", "chatbot", "algorithm", "machine learning",
"personal data", "data protection", "identity", "authenticat", "consent" (other than the TDRA's consent to
transfers) and "human" do not occur in either language (searched the extracted text of both licences on
2026-10-16). "Privacy" occurs once (9.2.1(b)); "personnel" twice (9.1, 12.6); "cyber" once (12.4). So the licence
carries no AI obligation. The press claim of "AI-readiness obligations" (tbreak, 2026-08-12) has no footing in the
text; what is new in 2026 is Article 12 (network resilience, diversified international connectivity, redundancy,
testing) and the twenty-year term. Treat the claim as dead.

**What binds the agent.** Clause numbers are the licence's own. Arabic is the extraction's text with the
lam-alef ligature restored.

| Clause | English (verbatim) | Arabic (verbatim) | Why it matters |
|---|---|---|---|
| 1.1.5 | "Customer means any Person who has made arrangements with the Licensee to receive Services from the Licensee under the Licensee's general terms and conditions" | "المشترك: يقصد به أي شخص تقدم بطلب للإستفادة من خدمات المرخص له وبموجب شروط تقديم الخدمة المعتمدة من قبل المرخص له" | The licence's "Customer" is the CPR's "Subscriber". |
| 1.1.14 | "Regulatory Framework means the policies, regulations, orders, resolutions; procedures, guidelines, determinations, directives, instructions and other such instruments as may be made or amended by the TDRA" | "الإطار التنظيمي: يقصد به السياسات واللوائح والأوامر والقرارات والإجراءات والإرشادات والمقررات والتوجيهات والتعليمات وغيرها من الأدوات التنظيمية المماثلة التي تصدرها الهيئة أو تعدلها" | **Guidelines are inside the Regulatory Framework.** Read with 3.2, a TDRA guideline binds the licensee through its licence even if the guideline calls itself non-binding. This does not reach the AI Ethics Principles and Guidelines (issued by the Minister of State for AI, not the TDRA; see section 4), but it would capture any TDRA AI guideline. |
| 2.2 | "The Licensee shall deploy and roll out its Telecommunication Network and related Services and provide and maintain service coverage in accordance with the TDRA's Regulatory Framework." | "يتعين على المرخص له نشر شبكة اتصالاته والخدمات ذات الصلة وتوسيع نطاقها، وتوفير تغطية الخدمة والمحافظة عليها وفقاً للإطار التنظيمي للهيئة" | Services, not only the network, must follow the Framework. |
| 3.1 | "The Licensee shall ensure that it complies with each of the terms and conditions set out in the License at all times during its term. The Licensee acknowledges that failure to comply ... may constitute grounds for suspension and/or revocation of the License and/or the imposition of fines and/or penalties" | "يتعين على المرخص له ضمان الالتزام بجميع الشروط والأحكام المنصوص عليها في الرخصة في جميع الأوقات طوال مدتها ... قد يشكل سبباً لتعليق الرخصة و/أو إلغائها و/أو فرض الغرامات و/أو الجزاءات" | The stakes. |
| 3.2 | "The Licensee shall comply with all laws of the UAE applicable to its operations, including but not limited to the Telecommunications Law. In addition, the Licensee shall comply with the Regulatory Framework and all directives of the Government of the UAE" | "على المرخص له الإلتزام بجميع القوانين في دولة الإمارات العربية المتحدة ذات العلاقة بأعماله بما في ذلك على سبيل المثال لا الحصر قانون الإتصالات. بالإضافة الى ذلك، على المرخص له الإلتزام بالإطار التنظيمي وجميع توجيهات الحكومة" | **The bridge clause.** PDPL, the Consumer Protection Law, the Cybercrimes Law, the Child Digital Safety Law and every TDRA instrument become licence conditions, enforceable by the TDRA under 16.3, not only by their own regulators. |
| 3.4.1 | "The Licensee may subcontract the provision of any or all of the Services and the installation, operation and management of the licensed network to an Affiliate or another Person ... with the prior written approval of the TDRA, provided that the Licensee shall continue to be fully liable for any obligations set out in this License or imposed on the Licensee pursuant to the Regulatory Framework ... If the Affiliate is and remains wholly owned by the Licensee or under the majority Control of the Licensee, the prior written approval of the TDRA shall not be required, provided that the TDRA shall always be notified" | "يجوز للمرخص له، بعد الحصول على موافقة خطية مسبقة من الهيئة، أن يعهد إلى تابع أو إلى شخص آخر من الباطن بتقديم أي من الخدمات أو جميعها وبتركيب الشبكة المرخصة وتشغيلها وإدارتها ... على أن يظل المرخص له مسؤولاً مسؤولية كاملة عن جميع الالتزامات" | Outsourcing the care channel to a vendor, or running it on a third party's model, keeps the operator fully liable; where the vendor "provides the Services" on the operator's behalf, prior written TDRA approval is required. Whether an AI vendor that only answers customers "provides the Services" is a classification question (inferred); the liability sentence is not. |
| 3.5 | "Quality of service for all Services offered by the Licensee shall meet or exceed the quality of service obligations contained in the Regulatory Framework in effect at the time." | "على المرخص له تزويد كافة الخدمات بدرجة جودة تعادل أو تفوق تلك المحددة بمعايير جودة الخدمة المتضمنة في الإطار التنظيمي النافذ" | QoS rules (section 4) apply to every channel. |
| 3.6 | "The Licensee shall not use or knowingly permit the use of its Services for any purpose that violates the Telecommunications Law or any other applicable laws or the Regulatory Framework ... The Licensee shall endeavor to take all reasonable action to ensure that its Services are not used for any such purposes." | "يجب أن لا يقوم المرخص له بإستعمال أو السماح، عن علم ومعرفة منه، باستعمال الخدمة لأي هدف يخالف قانون الإتصالات أو أية قوانين مرعية أخرى أو الإطار التنظيمي" | Standard of conduct. |
| 3.7 | "The prices that the Licensee may charge its Customers in connection with its Services, as well as the terms and conditions, are subject to regulation by the TDRA" | "تخضع الأسعار التي يجوز للمرخص له أن يفرضها على مشتركيه فيما يتعلق بخدماته والشروط والأحكام لتنظيم الهيئة" | An agent cannot invent a price or a term. |
| 8.2 | "The Licensee shall maintain calling party/called party details and subscriber information in accordance with any measures issued by any competent authority responsible for public interest, safety and national security ... install at its own expense any equipment required to allow access to its Telecommunication Network and/or the retrieval and storage of data" | "يتعين على المرخص له حفظ التفاصيل المتعلقة بالإتصالات سواء الواردة أو الصادرة بالإضافة الى المعلومات المتعلقة بالمشتركين وفقاً للمعايير الصادرة من الجهات المعنية والمسؤولة عن المصلحة العامة والسلامة والأمن الوطني" | Subscriber data retention and lawful access are licence duties; pairs with CPR 22.5 (security-authority disconnection). |
| 9.1 | "The Licensee shall maintain adequate trained personnel to receive and respond promptly to complaints and disputes from Customers. The Licensee shall take all reasonable action to promptly remedy and avoid the recurrence of the cause of all Customer complaints and disputes that relate to the quality, availability, delivery or billing of its Services. The Licensee shall also take all necessary measures to ensure that amounts due to Customers are paid promptly and in full." | "على المرخص له توفير ما يلزم من موظفين مدربين لتلقي والإجابة دون إبطاء على الشكاوى والمنازعات الخاصة بالمشتركين، كما يتعين عليه إتخاذ جميع الإجراءات المعقولة للمعالجة الآنية ولتجنب تكرار أسباب الشكاوى ونزاعاتهم ذات العلاقة بجودة الخدمة وتوفرها وتسليمها وفوترتها" | **Trained personnel (موظفين مدربين) for complaints is a licence condition, not only CPR 26.6.** Both languages say people. This is the licence-level twin of CPR 26.7.2. |
| 9.2.1 | "The Licensee shall prepare and publish a Code of Practice for the Licensee's Customers ... in accordance with the Regulatory Framework in effect at the time and shall contain at a minimum, information concerning the following: a) prices, terms and conditions of Service; b) privacy of Customer information; c) billing method and cycle; d) denial of service; e) cancellation and restoration of Service; f) subscriber contract; g) handling of complaints; h) options for directory listing information; and i) reserve for subscriber refunds and deposits." | "على المرخص له تحضير ونشر القواعد المهنية المتعلقة بمشتركيه ... أ) أسعار وشروط وأحكام الخدمة، ب) خصوصية المعلومات المتعلقة بالمشتركين، ج) أساليب الفوترة ودوريتها، د) حجب الخدمة، هـ) إلغاء وإعادة الخدمة، و) عقود الاشتراك، ز) معالجة الشكاوى، ح) خيارات لإدراج معلومات في الدليل، ط) احتياط المبالغ المعادة والودائع للمشتركين" | Every operator must publish a TDRA-approved Code of Practice covering privacy, denial of service, cancellation and complaints. The published codes are a source the report can cite for what e& and du promise today (not fetched; see section 8). |
| 9.2.2, 9.2.3 | "The Code of Practice shall be submitted to the TDRA for review and approval" ... "amended or replaced from time to time in accordance with any additions, deletions or modifications to the Regulatory Framework" | "يتعين على المرخص له تقديم القواعد المهنية إلى الهيئة لمراجعتها والموافقة عليها" | TDRA approval. |
| 9.2.4 | "The Licensee shall keep a record of all Customer complaints for a period no less than three (3) years or as otherwise specified in the Regulatory Framework" | "يتعين على المرخص له الاحتفاظ بسجل لجميع شكاوى المشتركين لمدة لا تقل عن ثلاث (3) سنوات، أو لأي مدة أخرى يحددها الإطار التنظيمي" | Three years here, two years in CPR 3.9; the licence's "or as otherwise specified" defers to the CPR. Log retention class for complaints: keep three. |
| 9.2.5 | "The Licensee shall make every reasonable effort to resolve disputes with its Customers in a timely manner." | "على المرخص له القيام بكل ما يلزم لتسوية شكاوى المشتركين لديه في وقت مناسب" | |
| 9.3 | "In the event of a dispute relating to the Code of Practice remaining unresolved ... or in certain cases when a complaint is referred directly to the TDRA, the TDRA may resolve the issues ... In all cases, the Licensee shall cooperate fully with the TDRA for the resolution of Customer complaints." | "وفي جميع الأحوال فإن على المرخص له التعاون الكامل مع الهيئة لتسوية شكاوى المشتركين" | The TDRA agent's standing in our build. |
| 9.4.2, 9.4.3 | "The Licensee shall ensure that bills are accurate and transparent." "The Licensee shall establish a procedure to ensure and validate the accuracy of its billing system. The Licensee shall retain all billing information for no less than two (2) years" | "على المرخص له ضمان تمتع الفواتير بالدقة والشفافية"; "يتعين على المرخص له وضع إجراء لضمان دقة نظام الفوترة لديه والتحقق منها" | A charge the agent adds on a bad consent breaks 9.4.2 as well as CPR 4.3. |
| 9.5.1 | "The Licensee shall ensure that Customers shall have free access to the emergency call service numbers designated by the TDRA for Emergency Calls." | "يتعين على المرخص له ضمان حصول المشتركين دون مقابل على خدمة الطوارئ على الأرقام المحددة من قبل الهيئة" | Twin of CPR 22.4. |
| 12.4 | "... redundancy, diversity, backup, disaster recovery and failover arrangements across its Telecommunications Network, including ... supporting systems ... in the event of equipment failure, network disruption, natural disaster, cyber incident or any other event" | "... أو وقوع كارثة طبيعية أو حادث سيبراني أو أي حدث آخر" | New in 2026. "Supporting systems" (الأنظمة الداعمة) plausibly includes customer-care systems (inferred). |
| 12.7 | "The Licensee shall comply with any directives, guidelines, or technical requirements issued by the TDRA from time to time in relation to network resilience, international connectivity, and continuity of critical Telecommunications Services." | "يتعين على المرخص له الالتزام بأي توجيهات أو إرشادات أو متطلبات فنية تصدرها الهيئة" | Guidelines again made binding. |
| 12.9.1, 12.9.2 | Planned interruptions (other than minor): inform the TDRA, interconnecting operators "and relevant Customers in advance ... the reason(s) for the interruption as well as the manner and time frames in which the interruption will be resolved"; unplanned: "as soon as possible" | "إعلام كل من الهيئة بالإضافة إلى المرخص لهم الآخرين والمشتركين المعنيين مقدماً بهذا الإنقطاع" | A service-interruption notice is a care-agent task with fixed content. |
| 13.5 | "The Licensee is permitted to use any technology for the installation and operation, management and maintenance of its Telecommunication Network and for the provision of its Services in accordance with the Regulatory Framework in effect at the time." | "يجوز للمرخص له استخدام أي تكنولوجيا لتركيب شبكة اتصالاته وتشغيلها وإدارتها وصيانتها وتقديم خدماته، وفقاً للإطار التنظيمي النافذ" | Technology neutrality: AI in the care channel is allowed, subject to the Framework. Nothing more. |
| 16.2 | "the order of precedence shall be in the following sequence: a) the Federal Law by Decree No. 3 of 2003 ...; b) its Executive Order ...; c) the Regulatory Framework in effect at the time; and d) the provisions of this License." | "أ) المرسوم بقانون إتحادي رقم 3 لسنة 2003 ... ب) اللائحة التنفيذية ... ج) الإطار التنظيمي النافذ، و د) نصوص الرخصة" | The CPR outranks the licence. |
| 16.3.2, 16.3.3 | "If the Licensee fails to comply with any of the following: a) any obligations under the Telecommunications Law or its Executive Order; b) any obligations within the License; or c) any obligations contained in the Regulatory Framework in effect at the time, the Licensee may be subject to a penalty. The penalty shall be not less than Dirhams 50,000 and not more than Dirhams 200,000"; doubled for repeat, missed deadline or material breach | "على أن تتراوح قيمة الغرامة بين 50,000 درهم كحد أدنى وبين 200,000 درهم كحد أقصى"; "يمكن مضاعفة الغرامة" | The licence-level penalty for a CPR breach: AED 50,000 to 200,000, doubled; the law's 79 bis (2) ten-million route sits above it. |
| 16.6 | "The License shall replace and supersede the previous License issued to the Licensee under License No. 1/2006." (3/2026: "License No. 2/2006") | "تحل هذه الرخصة محل الرخصة السابقة الصادرة للمرخص له بموجب الرخصة رقم 1/2006 وتلغيها" | The 2006 licences are dead text. |
| 16.7 | "The Arabic language version of this License is the binding version. However, an official English language version has been prepared for guidance, and assistance in interpretation of the Arabic language version." | "تعتبر اللغة العربية للرخصة هي الملزمة وعلى الرغم من ذلك فقد تم إصدار الرخصة باللغة إنجليزية رسمية للتوجية والمساعدة في تفسير النسخة باللغة العربية" | Quote Arabic when it matters. The CPR has no such clause (open point from 2026-10-15); the licence does. |

Clauses read and set aside as not touching the agent: 1.1.1 to 1.1.4, 1.1.6 to 1.1.13, 1.1.15 to 1.1.20, 1.2,
2.1, 3.3, 3.4.2 to 3.4.4, 3.8, Article 4 (royalties, fees, the 1 percent development fund fee), Article 5
(books, ten-year financial records, audit), 6.1 to 6.4 (operational reporting, QoS results reporting under 6.1.1,
TDRA access to premises and information), Article 7 (anti-competitive practices; 7.1(g) bars use of Customer
information where the object or effect is anti-competitive), 8.1, 8.3, 9.4.1, 9.5.2, Article 10 (interconnection,
10.1.8 cooperation on shared Customers), 11, 12.1 to 12.3, 12.5, 12.6, 12.8, 12.10 to 12.12, 13.1 to 13.4
(13.2 CLI transmitted "transparently and without any alterations"), 13.6, Article 14 (spectrum), Article 15
(term, renewal 180 days before expiry, modification, suspension, revocation, termination), 16.1, 16.4, 16.5.

## 4. Every other rule found that binds the agent

### 4a. Found and read by me

**Federal Decree-Law No. 26 of 2025 Regarding Child Digital Safety.** Binding. Issued 2025-10-01, in force
2026-01-01 (Art 20); everyone subject to it has one year to regularise (Art 18), so full compliance falls due
2027-01-01 (inferred from the two articles). None of our earlier files mention it. Who it binds: "Internet
Service Provider: Any licensed person, pursuant to Federal Decree by Law No. (3) of 2003 ... who provides users with
access services to the information network" (Art 1), so e& and du; and "Digital Platform: An electronic means
that enables interaction and communication among users in the digital space and provides digital services or
content" (Art 1), which on its words takes in an operator's self-care app (inferred). Scope Art 3(1): ISPs and
digital platforms "whenever Children use digital platforms or are exposed to their content or services".

| Clause | English (verbatim) | Arabic (verbatim, read from the portal PDF) | Why it matters |
|---|---|---|---|
| 7(1) | "digital platforms ... shall be prohibited from collecting, processing, publishing, or sharing the personal data of Children under the age of thirteen (13), unless the following conditions are fulfilled and verified: a. Obtaining parental consent from the child caregiver, provided that such consent is explicit, documented, and verifiable. b. Providing a rapid and continuously accessible mechanism for withdrawing parental consent ... d. Restricting access to personal data to authorized persons only within the digital platform and to the minimum extent necessary for service provision. e. Refraining from using the data for commercial purposes, for the purpose of providing targeted electronic advertising to the child" | not compared | A care agent that processes a child's data (a child's line in a family plan, a minor caller) needs a verified caregiver consent on file. |
| 8 | "Digital platforms ... shall be required to adopt effective and reasonable age-verification mechanisms, standards, and procedures, in accordance with the classification of digital platforms pursuant to the system referred to in Article (6)" | not compared | The verification standard is delegated to a Cabinet classification system (Art 6), not yet found. |
| 9(2) | "Digital Platforms and Internet Service Providers shall be required to take the necessary technical and administrative measures to prevent Children's access to games prohibited under this Article, including age-verification mechanisms, Parental Control Tools, and blocking Harmful Content." | not compared | An ISP duty in the law itself, not waiting on the TDRA. |
| 11(1) | "The Authority shall issue policies, standards, and regulatory instructions specifying the obligations of Internet Service Providers related to ensuring Child digital safety ... including the following obligations: a. Activating content filtering systems within networks ... b. Taking the necessary measures to ensure safe and supervised use where the beneficiary of internet services or Electronic Devices is a Child, including requiring the Child Caregiver to sign service terms, including those mandating linkage of the service to Parental Control Tools. c. Providing guidance tools and software enabling Parental Control Tools ... d. Immediately reporting to the Concerned Authorities any Child Pornography Materials or Harmful Content" | "تُصدر الهيئة السياسات والمعايير والتعليمات التنظيمية التي تُحدد التزامات مزودي خدمات الإنترنت المتعلقة بتحقيق السلامة الرقمية للطفل وحمايته من المحتوى الضار في البيئة الرقمية، شاملاً الالتزامات الآتية: أ. تفعيل أنظمة تصفية المحتوى في الشبكات ... ب. اتخاذ التدابير اللازمة لضمان استخدام آمن وخاضع للرقابة في حال كان المستفيد من خدمات الإنترنت أو الأجهزة الإلكترونية طفلاً، بما في ذلك إلزام القائم على رعاية الطفل بالتوقيع على شروط الخدمة بما فيها تلك التي تفرض ربط الخدمة بأدوات التحكم الأبوي. ج. توفير أدوات وبرمجيات إرشادية تتيح التحكم الأبوي ... د. الإبلاغ الفوري للجهات المعنية" | **Where the beneficiary of the service is a child, the caregiver signs the service terms.** So an agent that activates or changes a service must know whether the user is a child and, if so, deal with the caregiver. The TDRA instructions that spell this out were not found (searches in both languages, 2026-10-16); until they exist the duty is the law's own words plus Art 11(2). |
| 11(2) | "The Authority shall review the policies of Internet Service Providers and supervise and monitor their compliance" | "تقوم الهيئة بمراجعة سياسات مزودي خدمات الإنترنت والإشراف والرقابة على مدى تنفيذهم للالتزامات" | TDRA is the supervisor, so a breach is also a licence matter (licence 3.2). |
| 10(1)(g) | platforms shall provide reporting tools "and leveraging their technical capabilities, including artificial intelligence systems and machine learning algorithms, for proactive detection, removal, or reporting" of harmful content | not compared | The law's only mention of AI: a use the State wants, for detection. Nothing on AI that talks to children. |
| 16, 18, 20 | Administrative penalties by a Cabinet regulation (not found); one year to regularise; in force 2026-01-01 | | |

**Cabinet Resolution No. 106 of 2026 Regulating Children's Access to Social Media Platforms.** Binding on social
media platforms (Art 2: every platform whose services are available in the State or directed at users in it), not on an
operator's care channel. Issued 2026-06-17; in force the day after Gazette publication (Art 9); platforms get
twelve months to comply (Art 8(1)). Worth one paragraph because Article 4 is the first UAE text that says what
counts as acceptable verification of a person: 4(2) lists "التحقق من خلال الهوية الحكومية الرقمية، أو مسح الهوية
الرسمية، أو أي وثيقة رسمية مع المطابقة البيومترية" (verification through the government digital identity, or
scanning the official identity or any official document with biometric matching), "تقنيات تقدير العمر باستخدام
الذكاء الاصطناعي، بما في ذلك الوسائل البيومترية" (AI age-estimation techniques including biometric means),
"مزودو خدمات التحقق من العمر المعتمدون والمرخصون في الدولة" (approved and licensed age-verification providers);
4(3) "لا يُعتد بالتصريح الذاتي بالعمر، أو بأي آلية أخرى للتحقق من العمر غير معتمدة" (self-declaration of age is not
accepted); 4(1)(c) data minimisation and no retention of biometric data beyond the verification; 7(2) the TDRA
supervises the platforms' technical compliance. It is a benchmark for gap 5, not a rule for it.

**Cabinet Resolution No. 56 of 2024 Concerning the Telemarketing Regulations, and No. 57 of 2024 on its
violations and penalties.** Binding. Both issued 2024-06-10, in force sixty days after Gazette publication (Art 11
of 56, Art 7 of 57); the portal lists 57/2024 as effective 2024-08-27 and the press gives the same date for both.
Issued under, among others, the Telecom Law, the Consumer Protection Law and the PDPL (preamble). None of our
earlier files mention them. Scope, Art 3(1): "The provisions of this resolution shall apply to all companies
licensed in the State, including those located in free zones, that market products or services through
telemarketing." "Telemarketing: Phone Calls made by a company or a natural person to a Consumer for marketing,
advertising or promoting the products or services they provide ... including marketing text messages and marketing
messages through social media applications"; "Consumer: Natural Person" (Art 1). So an operator's outbound upsell
calls and marketing SMS to subscribers are inside it (inferred from the definitions; the text names no sector
exception for telecom operators, and the TDRA runs the Do Not Call Registry under Art 1 and coordinates under Art 8).

| Clause | English (verbatim) | Arabic (verbatim, extraction with ligatures restored) | Why it matters |
|---|---|---|---|
| 4(7) | "Record Marketing Phone Calls, with the necessity of informing the Consumer of this recording when the call begins." | "تسجيل المكالمات الهاتفية التسويقية، مع ضرورة إشعار المستهلك بهذا التسجيل عند بدء المكالمة." | Recording notice at the start. Fine (57/2024 Table 1, rows 6 and 7): AED 10,000, 25,000, 50,000 for not recording; 10,000, 20,000, 30,000 for not announcing it. |
| 4(11) | "Identify the Company and the purpose of the call at the beginning of the marketing Phone Call." | "التعريف عن هوية الشركة والغرض من الاتصال عند بداية المكالمة الهاتفية التسويقية." | Company and purpose, not the nature of the caller. Row 9: AED 10,000, 20,000, 30,000. |
| 5(1), 5(2) | "Not to use any marketing methods that put unjustified pressure on the Consumer"; "Avoid deception and misleading when marketing" | "عدم استخدام أي وسائل تسويقية تشكل ضغوطاً غير مبررة على المستهلك"; "الابتعاد عن الخداع والتضليل" | Rows 11, 12: up to AED 50,000 and 75,000. Pairs with CPR 28.25. |
| 5(3) | "Make Marketing Phone Calls only during the period from 9:00 am to 6:00 pm." | "إجراء المكالمات الهاتفية بغرض التسويق خلال الفترة من 9:00 صباحاً وحتى 6:00 مساءً فقط." | Row 13: AED 10,000, 25,000, 50,000. A gate the agent can check by clock. |
| 5(4), 5(5) | No call back after a refusal on the first call; no more than one call-back a day and two a week when unanswered or ended | "عدم معاودة الاتصال بالمستهلك في حال رفضه للمنتج أو الخدمة في المكالمة الأولى" | Rows 14, 15. |
| 5(6) | "Automated communication systems may be used for marketing, advertising and promoting the products or services provided by the Company in accordance with the provisions of this resolution." | "يجوز استخدام أنظمة الاتصال الآلي للتسويق والدعاية والترويج للمنتجات أو الخدمات التي تقدمها الشركة وفق أحكام هذا القرار." | **The one UAE clause that expressly permits automated calling systems to market to consumers.** It attaches every duty of Articles 4 and 5 to the machine and adds none about disclosing that it is a machine. 57/2024 row 16 fines "Using automatic calling or marketing, promotion and advertisement of products or services provided by the company in violation of provisions of this Resolution": AED 10,000, 25,000, 50,000. |
| 5(7) | "Ask the Consumer whether he wants to continue the Phone Call or not before starting to market, advertise and promote the product or service provided." | "سؤال المستهلك عن مدى رغبته في استكمال المكالمة الهاتفية من عدمه قبل البدء بالتسويق والدعاية والترويج للمنتج أو الخدمة المقدمة." | A consent-to-continue step before any pitch. Row 17: AED 10,000, 20,000, 30,000. |
| 4(5), 6(5) | No calls to numbers on the DNCR; the consumer may register on the DNCR | "عدم الاتصال بغرض التسويق للمنتجات أو الخدمات للمستهلكين الواردة أرقامهم في سجل عدم الاتصال" | Row 4: AED 50,000, 75,000, 150,000. |
| 6(4) | "Consumer personal data may not be disclosed without his consent or to trade it for reprocessing it by companies wishing to market their products or services to the Consumer through Marketing Phone Calls." | "يُحظر الكشف عن البيانات الشخصية للمستهلك دون موافقته أو الإتجار فيها لأغراض إعادة معالجتها من قبل الشركات التي ترغب في التسويق" | Row 18: AED 50,000, 75,000, 150,000. Pairs with CPR 24.6 and PDPL. |
| 4(1), 4(2), 4(3), 4(6), 4(8), 4(12) | Prior approval to practise phone marketing; training of marketers; local registered numbers; a register of all marketing calls on the authority's form; periodic reports; disclose the source of numbers on request | | Rows 1, 2, 3, 5, 8, 10. |
| 57/2024 Art 3 First | Penalties on companies: warning; the fine; suspension of activity 7 to 90 days; cancellation of licence, deletion from the commercial register, "cutting communications services and removing the phone number"; most severe penalty on repetition within six months | | |

Supervision (56/2024 Art 9): the Ministry of Economy in general; the Central Bank for banks and insurers; the
Securities and Commodities Authority for securities; the local licensing authorities for other companies. Which
"Competent Authority" approves a telecom operator's own telemarketing is not stated in the text (for a
federally licensed operator it reads as the TDRA; inferred).

**Supreme Committee Resolution No. 3 of 2004 issuing the Executive Order.** The licence puts it above the
Regulatory Framework (16.2(b)) and the law's documents rule (72 bis (5)) points to it. Only its cover page is
published. Not read.

**The Cabinet schedule of licensee violations and fines promised by Telecom Law Art 79 bis (2).** Not found on
the legislation portal or by search in English and Arabic on 2026-10-16. The only telecom fine schedules found
are the telemarketing ones above.

**e& Customer Service Charter (etisalat.ae, PDF dated 2024-06-04).** Not a rule; the operator's own published
promise, citable as what e& tells customers today: "We will have helpful and professional team members capable
to fulfill your needs"; "We will safeguard your personal information and ensure secure interaction at all our
touch points"; "If you wish to make a formal complaint, please contact our Customer Care Centre available 24
hours a day, 7 days a week ... Our customer service representatives are highly trained to help in resolving your
concerns and complaints promptly. If your complaint was not resolved, our customer service representatives will
lodge a formal complaint on your behalf." It refers to a Code of Practice on etisalat.ae; the host that serves
it (support.etisalat.ae) refused connections from here on 2026-10-16, and du's Code was not found by search.
File: `standards-text/etisalat-customer-service-charter-2024-en.pdf/.txt`.

### 4b. From the three research agents (verbatim clauses, URLs and fetch dates are in their notes)

Notes: `research-notes/uae-rules-2026-10-17/data-and-cyber.md`, `consumer-contract-ai.md`,
`tdra-and-licences.md`. Status as of 2026-10-17.

| Instrument | Binding? | What it adds for the agent (clause) |
|---|---|---|
| PDPL, Federal Decree-Law 45/2021 (in force 2022-01-02; binds operators as "Establishments", Art 1; Arabic prevails) | Yes, but its Executive Regulations (Art 28), penalties decision (Art 26) and grace period (Art 29) were never issued; the Data Office never became fully operational and was absorbed 2026-06-14 into a new Federal Authority for AI and Data (press and law-firm notes; founding instrument not found) | 18(1) Arabic confines the objection right to decisions with legal consequences or serious effect (تبعات قانونية أو تؤثر بشكل جسيم): disconnection qualifies, a declined add-on probably not. 18(4) unconditional in both languages (يتعين على المتحكم إدخال العنصر البشري ... بناءً على طلب صاحب البيانات). 21(2)(a) DPIA and 10(1)(a) DPO mandatory before such processing. 6(1)(b) consent "in writing or electronically" (كتابية أو إلكترونية); spoken not named. 13(1)(c) information on automated decisions only on request; 13(2) excludes it from the pre-processing notice. A hosted LLM is a Processor (Art 1): 7(5), 8(1) contract content, 8(4) erasure, 8(5) no disclosure of results, 8(10) joint liability, 23(1)(a) contract route, 13(2)(d) and (g) tell the subscriber who receives the data abroad; Art 22 adequacy approvals, 23(2) controls and 8(11) standards absent. Art 9 breach notification has no period. |
| Cybercrimes, Federal Decree-Law 34/2021 (in force 2022-01-02) | Yes, criminal | 6(1) disclosure of data after weak verification (bank and e-payment data aggravating); 45 confidential information obtained at work; 13 processing in violation of legislation; 44(1) consent to record conversations (pairs with CPR 4.17.3); 48 a false price in a promotion; 40 false impersonation, fraud cases only. |
| TDRA Information Assurance Regulation v1.1 (2020) | Mandatory only for entities designated critical under the unpublished CIIP list; voluntary otherwise | T6 third-party agreements. Reported successors (Cyber Security Council IA Standard v2.0, 2025; National Cyber Security Policy for AI v1.1): texts not obtainable (csc.gov.ae refuses connections). No federal cybersecurity decree-law 2023 to 2026; no data-localisation rule outside health data (Federal Law 2/2019). |
| Consumer Protection Law 15/2020 as amended by 5/2023 (in force 2020-11-11) and Cabinet Decision 66/2023 (in force 2023-10-14) | Yes; applies to telecom with no TDRA carve-out; the CPR does not cite it | 4(5) confirmed both languages; 8(4) and 26 with 66/2023 Addendum 2 rows 13 and 14: data, advertisements and contracts in Arabic (AED 100,000), harmful terms AED 250,000, misleading description AED 250,000 and Art 29 prison up to two years. 66/2023 Art 34(1), (3), (5): void any term letting the supplier alone judge conformity, terminate unilaterally, or change a subscription service unilaterally (exception: notified upgrade or outside cause). |
| Electronic Transactions and Trust Services, Federal Decree-Law 46/2021 (in force 2022-01-02); Cabinet 28/2023 executive regulations and 52/2024 penalties exist, not read (portal down) | Yes | **Art 11(2): a contract made through an automated electronic system binds the person only if the person "knows, or is supposed to know, that such system will make or execute the contract automatically."** Arts 10, 12(2)(b), 28(1): consent elicited by the system is consent; the system's messages are the operator's. Art 33: low, medium and high trust levels; 33(4)(d) the TDRA sets "Authentication Procedures to confirm the identity of any person to the Relying Party", for public and private services (33(4)(e)). |
| Decree-Law 14/2023 on trading by modern technological means (in force 2023-09) and Cabinet 200/2025 penalty schedule | Yes; whether it reaches an operator selling by app or chat is inferred, unconfirmed | 10(2)(a) consumer data "may not be shared with any other person unless ... legally justified or based on the prior approval of the consumer"; 13(2) and the 200/2025 violation for failing to verify "صفة وهوية المتعاقدين" (the capacity and identity of the contracting parties). |
| UAE AI Charter (public policy, 2024-06-10); AI Ethics Principles and Guidelines (Dec 2022, "non-binding", 3.3.2.2 with the conversational-agent example); Deepfake Guide 2021; Dubai 2019 guidelines, DCAI and AI Seal; Abu Dhabi Laws 3/2024 and 5/2025 (a policy council); CBUAE AI guidance 2026-02-23 (banks only) | None binds an operator | Cabinet agentic-AI framework of 2026-05-18: confirmed, unnumbered, federal entities only, text unpublished, nothing on disclosure or oversight. No federal AI law (Al Tamimi 2026-09-01). AI and Data Authority announced 2026-06-14. Stated practice since: "human leads, AI enables" (2026-08), an Agent Control Tower and a "life and livelihood" red line (Minister Al Olama, 2026-10-15). |
| TDRA register 2023 to 2026: 113 documents EN, 94 AR; 29 EN and 23 AR dated 2023 to 2026; five touch customer interaction | Regulatory Framework, so binding through licence 3.2 | **Spam Calls Policy v4.0** (issued 2025-10-14): 3.3(iii) a Telemarketing Call is audible "regardless of whether ... the audible message contains a natural or a synthesised voice"; DNCR default enrolment 9.5, DNCR check 10.2, hours 15.4, black points 13.4, Cabinet 56/2024 imported by 5.4; 14.3 the consent gate ("audible warning" plus "specific action to confirm his/her consent" before call set-up); Spam SMS 5.6 the consent record ("date, time, words or other content by which the Customer indicates their Consent and identity"). **QoS Policy v3.0** (issued 2024-07-11): T1(2a), the only customer-service KPI, "from the time the Customer has selected the IVR choice to speak to an agent until the Customer is connected to an agent", under two minutes average, indicative (6.6, 9.5); no complaint, chat or app indicator. **Decision 16/2026 on use of mobile devices** (issued 2026-05-11, Arabic only): 4.17 and 4.18 on a loss or theft report (a call counts, 1.22) the licensee must "verify the reporter's identity" and block the device within two hours, free (4.19); how to verify is unsaid. **Instructions 1/2014** (Arabic only): WCAG 2.0 apps and staff trained for People of Determination. Verification texts are counter-based only: 2011 Registration Policy 6.1, Annex 4 (2020) 7.9. No TDRA instrument on AI, chatbots, UAE Pass or biometric verification, caller-ID spoofing, or Child Digital Safety Art 11, in either language. Register dates are upload dates. |
| The renewal press release (TDRA, 2026-08-12, EN and AR, "digital-infrastructure-and-the-digital-economy") | Official statement, not text | Obligations named: network resilience, backup capacity, international connectivity, QoS, interconnection and access, national roaming, universal service, subscriber protection, anti-competitive practices. The only AI sentence is Belhoul's "intelligent, autonomous networks". tbreak's "AI-readiness" line cites no clause. The 2006 licences (now on disk, bilingual): 9.1 and 9.2 are word for word the 2026 text; the Regulatory Framework definition grew from "guidelines and other such determinations" (2006 1.1.16) to add "directives, instructions" (2026 1.1.14). |

## 5. The eight gaps re-checked (settled 2026-10-17, Fable)

Each verdict rests on sections 2 to 4. Where a clause is quoted only in an agent's notes, the notes file is
named. "Kept" means no text closes it.

1. **No duty to tell a consumer they are talking to an AI. KEPT for the conversation, NARROWED for sales.**
   No general duty anywhere: the law, the licence, every TDRA instrument, the PDPL (13(1)(c) only on request)
   and the Consumer Protection Law are silent, and the two texts that expressly contemplate machines talking to
   consumers, Cabinet 56/2024 Art 5(6) and Spam Calls v4 3.3(iii) ("a natural or a synthesised voice"), demand
   company, purpose and recording disclosures but not the machine. The one binding hook is Electronic
   Transactions 46/2021 Art 11(2): a contract made through an automated system binds the person only if they
   "know, or are supposed to know" that the system makes or executes it. So before any purchase through the
   agent, disclosure is a validity condition of the sale; for service, data and complaint conversations the gap
   stays whole. The non-binding Ethics guideline 3.3.2.2 remains the only text that says it outright.
2. **What an automated channel must do when a conversation becomes a complaint. NARROWED further.** The
   trigger (CPR 2.1.7) and the human requirement are now double-sourced: licence 9.1 "adequate trained
   personnel" (موظفين مدربين), unchanged since 2006, applies at licence level to every channel, which ends the
   26.7.1 versus 26.7.2 channel argument. What stays missing: the mechanics (stop, hand over, how fast). QoS
   v3.0 T1(2a) measures only the wait after "the IVR choice to speak to an agent" (under two minutes, indicative),
   so a bot that sits before that choice is unmeasured, and there is no chat or app indicator.
3. **"Only two AI clauses." CORRECTED stands, restated.** Across every binding text read, AI or automation is
   mentioned five times (CPR 25.14 and 26.7.2, Spam Calls v4 3.3(iii), Cabinet 56/2024 5(6), Child Digital
   Safety 10(1)(g)) and a conduct standard for it is set zero times. State it as five mentions, no standard.
4. **Automated disconnection: no human-review right. NARROWED.** The CPR still has none. The PDPL side is now
   precise: Arabic 18(1) confines the objection right to decisions with legal consequences or serious effect,
   which disconnection meets; 18(4) human review on request is unconditional in both languages; 21(2)(a) DPIA
   and 10(1)(a) DPO are mandatory first. The contract escape in 18(2) is undercut by Cabinet 66/2023 Art 34(1),
   (3) and (5), which void any term letting the supplier alone judge conformity, terminate or change a
   subscription unilaterally (inferred interaction between the two instruments; quote both). What stays a gap:
   no procedure, no deadline and no regulator for the review, because the PDPL Executive Regulations were never
   issued.
5. **"Adequate verification" (CPR 24.10) undefined. KEPT, sharpened to a sentence.** No UAE text defines it for a
   remote channel: TDRA verification rules are counter-based (2011 Registration Policy 6.1, Annex 4 7.9);
   Decision 16/2026 4.17 orders the licensee to "verify the reporter's identity" on a loss report without saying
   how; Electronic Transactions Art 33 supplies the vocabulary (low, medium, high trust levels, and 33(4)(d) TDRA
   "Authentication Procedures to confirm the identity of any person") that nobody has mapped to 24.10; Cabinet
   106/2026 Art 4 lists accepted means and rejects self-declaration, for platforms' age checks only. The cost of
   getting it wrong is criminal (Cybercrimes 6(1), 45; Telecom Law 72(2)) and the attacker's act is a crime
   (Telecom Law 72 bis (4); Cybercrimes 40), yet the operator's duty of care has no standard.
6. **The 2026-05-18 Cabinet agentic-AI framework. CONFIRMED as recorded.** Unnumbered, federal ministries and
   entities only, text unpublished, nothing on disclosure or oversight. No federal AI law exists; the Federal
   Authority for AI and Data (announced 2026-06-14) has issued nothing. Not a gap in the CPR sense; a fact to
   state once.
7. **Consent elicited by an AI. NARROWED.** Electronic Transactions Arts 10, 12(2)(b) and 28(1) settle that
   consent given to the system is consent and the system's words are the operator's; Art 11(2) adds the
   knowledge condition (gap 1). For outbound marketing the gate is written: 56/2024 Art 5(7) consent to continue,
   Spam Calls v4 14.3 ("audible warning" plus "specific action to confirm") and Spam SMS 5.6 for the record. What
   stays: the CPR medium classification (4.17, 4.22, 4.10) that decides whether an OTP is needed, and PDPL
   6(1)(b), which names consent "in writing or electronically" and not spoken, so a spoken consent through an
   AI covers the purchase (CPR 4.7.2) but not a new processing purpose.
8. **Subscriber data sent to a hosted model provider. PROMOTED from candidate to KEPT.** The provider is a
   Processor (PDPL Art 1) and the rules exist (7(5), 8(1), 8(4), 8(5), 8(10), 23(1)(a); 13(2)(d) and (g) notice of
   the foreign recipient; 14/2023 10(2)(a) prior approval; Telecom Law 72(2) reaches anyone "connected by a
   relationship that allows access"; licence 3.4.1 keeps the operator fully liable and needs TDRA approval where
   the vendor provides the Services); the machinery does not (Art 22 adequacy list, 23(2) controls, 8(11)
   standards, all waiting on Executive Regulations never issued). Rule present, machinery absent.

## 6. New gaps and candidates from this read

9. **A child on the line.** Child Digital Safety 7(1) (verified caregiver consent for under-13 data) and 11(1)(b)
   (the caregiver signs the service terms where the beneficiary is a child); the agent has no age signal, and the
   Cabinet classification (Art 6), the TDRA instructions (Art 11) and the penalties (Art 16) are unpublished.
10. **Outbound marketing by the agent** is fully written: 56/2024 Arts 4 and 5, Spam Calls v4 (DNCR 9.5 and 10.2,
    hours 15.4, consent gate 14.3), with fines per row of 57/2024. A ready-made gate set, not a gap.
11. **The Executive Order** sits above the Regulatory Framework (licence 16.2(b)) and is unpublished.
12. **Arabic records.** Consumer Law 4(5), 8(4) and 66/2023 Addendum 2: data, advertisements and contracts in
    Arabic, AED 100,000; an English-only chat transcript may not satisfy it (inferred).
13. **Accessibility.** Instructions 1/2014: WCAG 2.0 apps and staff trained for People of Determination; pairs
    with Telecom Law 30 and Readiness dimension 6.
14. **The upgrade test.** 66/2023 Art 34(5) voids unilateral service changes except a notified upgrade; a sharper
    gate than CPR 4.4's three conditions.
15. **A hallucinated price is a crime.** Consumer Law Art 29 (prison up to two years) and Cybercrimes 48, on top of
    CPR 3.3 and 5.3 and licence 9.4.2.
16. **Loss or theft reports.** Decision 16/2026 4.17 to 4.19: verify identity, block within two hours, free. A
    new scenario with a verification hole inside it.
17. **Breach notification without a period.** PDPL Art 9; the Executive Regulations that would fix it do not exist.

## 7. What changes in the build

- **Disclosure gate before any sale:** the agent states that it is an automated system before a purchase step and
  logs the statement (46/2021 Art 11(2)); the ungoverned agent sells without it, and the report shows the
  contract's validity in doubt, not only a breach.
- **Complaint hand-over cites two sources:** CPR 26.7.2 and licence 9.1; log the IVR-equivalent moment so the
  QoS v3.0 T1(2a) clock can be shown.
- **Disconnection gate adds the PDPL and 66/2023 layer:** DPIA on file (21(2)(a)), human review on request
  (18(4)), no reliance on a unilateral-termination term (66/2023 34(1); corrected from 34(3) on 2026-10-21 after the blind keys review: 34(3) is the conformity term).
- **Verification gate declares its level:** classify each disclosure request by Electronic Transactions Art 33
  trust level and refuse account data below the level the policy adviser sets; log the level, and present the
  missing mapping as the gap.
- **Outbound marketing module:** clock (9:00 to 18:00), DNCR check, company and purpose, recording notice,
  consent to continue, no call-back after refusal, call register, all from 56/2024 and Spam Calls v4.
- **Child check:** age or caregiver flag on the account before any change or data disclosure (Child law 7(1),
  11(1)(b)); absent flag, treat as unverified.
- **Model-provider gate:** the minimum, de-identified payload, a processor contract on file (PDPL 8(1)), the
  foreign-recipient notice (13(2)(d), (g)); log what left (unchanged) and cite 72(2).
- **Records:** complaints three years (licence 9.2.4), billing two years (9.4.3), consent and 2FA five years
  (CPR 3.9); Arabic copy of every record that is a contract or notice (Consumer Law 8(4)).
- **Price gate unchanged, citation upgraded:** quoted figures must come from the KB; cite Consumer Law 29 and
  Cybercrimes 48 beside CPR 3.3.

## 8. Not read or not covered (as of 2026-10-17 04:30 Amman)

- The agents' own "not read" lists in their three notes files, in short: PDPL Executive Regulations and penalties
  decision (never issued); any Data Office guidance (none found); the founding instrument of the Federal Authority
  for AI and Data; the Cyber Security Council's IA Standard v2.0, AI security policy, CIIP Policy and critical-entity
  list (csc.gov.ae unreachable); Cabinet 28/2023 and 52/2024 under the Electronic Transactions law (portal down);
  the 200/2025 fine amounts (Arabic unreadable); the AI Charter PDF, the Deepfake Guide, the CBUAE note (blocked);
  the Arabic Spam Calls v4 text layer (defective, flagged for checking against page images); the Licensing
  Regulation 2023 (image-only).
- The Executive Order of the Telecom Law (Resolution 3/2004): only the cover page is published.
- The Cabinet schedule of licensee violations and fines under Telecom Law Art 79 bis (2): not found.
- The TDRA instructions to ISPs under Child Digital Safety law Art 11, the Cabinet classification system under
  its Art 6 and its penalties regulation under Art 16: not found by search in either language.
- Cabinet Resolution 106/2026 in English (portal refused the download; Arabic read in full).
- The e& Code of Practice for Customer Affairs (host refused connections; the Internet Archive copy failed) and
  du's Code of Practice (not found by search).
- The Arabic Telecom Law beyond Articles 13, 14, 72 to 79 bis; the Arabic licence text beyond the clauses in
  section 3 (the bilingual file holds it all); the Arabic Child Digital Safety law beyond Article 11.
- Telecom Law articles not quoted in section 2 were read but not compared in Arabic.
- Whether the TDRA's 2022 print edition differs anywhere from the portal's 2020 consolidation: not compared
  page by page (both have the same amendment set; the 2022 edition is image-only).
- The Official Gazette dates that fix the in-force dates of 56/2024, 57/2024 and 106/2026: not checked.
