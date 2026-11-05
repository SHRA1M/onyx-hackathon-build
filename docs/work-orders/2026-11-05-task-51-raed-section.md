## Task 51, added 2026-11-05: Ra'ed Shraim's review

Appended by Opus from `raed-review-ruling-2026-11-05-fable.md` sections 1.3 to 1.5, 2.1 and 3 (Iyas: "we do what Fable decides"). Wording and data notes only: no gate logic, scenario, run, key or chunk change. Fit check against main 7de5b3f: `D:\Projects\engineering\onyx-hackathon-build\docs\report-back\2026-11-05-raed-ruling-fit-check.md`. **HELD means the fit check found the ruled text false or unbuildable: do not build it until hq answers the named question there.** The filed order under `docs/work-orders/` is frozen: file this section as its own dated file. Anything Iyas's eye-check list changes follows from the source page, never from memory; a wrong quote in a frozen key is a stop.

Added to Done means 7: `onyx/data/rules.json` (`language_note` of cpr-26-7-2, note of licence-3-4-1 only), the README reviewer row. Added to Done means 1: the `git grep` for 51.H item 4.

### 51.H CPR 26.7.2 (ruling 1)

1. **HELD on the place only, question 3.** Gap 1, the annex rule sample, the S2 hand-over narrative: quote 26.6, the 26.7 chapeau, 26.7.1 and 26.7.2 together in both languages, then this note, as ours: "The English 26.7.2 is an active prohibition ('preclude'). The Arabic is a passive exclusion, 'excepted or excluded from them', whose antecedent is the chapeau, 'the provisions of sub-article 26.6', a duty to keep trained personnel for complaints. TDRA's own English rendering reads the exclusion as a bar, and licence 9.1 (Arabic binding, licence 16.7) independently requires trained personnel to receive and respond to complaints. The CPR does not say which language prevails. Mizan enforces the stricter reading and cites the chapeau, the clause and licence 9.1 together." Source: `standards-text/tdra-cpr-v2-en.txt` 3414 to 3425, `tdra-cpr-v2-ar.txt` 1816 to 1826; chapeau in `kb/chunks-full/` only, eye-check block 89. Ra'ed's drop-in ("both readings reach the same result", "the Arabic prevails under the portal's own note") does not go in.
2. `rules.json` cpr-26-7-2 `language_note`: rewritten to the same effect, shorter; `quote_ar` stays verbatim. `docs/annex.md` line 115 follows. Source: ruling 1.4.
3. **HELD, question 4.** A rule row for the 26.7 chapeau: ruled only if `check-data` accepts it without touching chunk files; `kb/chunks` has no 26.7.
4. "The portal says the Arabic prevails" about the gate table or the CPR: none on main (fit check). Confirm by `git grep -i prevail`; the per-instrument truth is licence, 16.7 binding Arabic; PDPL and portal laws, portal note; CPR, not stated. Source: ruling 1.5.

### 51.I Report limits (ruling 2.1 and 3)

**All of 51.I is HELD on length, question 3: main text stays 5 pages and page 5 has no free line.**

1. **HELD on wording too, question 2.** Arabic coverage paragraph, ruled text: "Arabic coverage is uneven. The CPR, the licence and TDRA Decision 16/2026 are chunked in both languages. The PDPL Arabic is on file and quoted in the gap register but not chunked, so the recorded runs log 'no Arabic text on file' for PDPL clauses and gaps 2, 4 and 5 rest on the English text. The Arabic scenario lines are written in Modern Standard Arabic; dialect handling is untested." Ra'ed's "the PDPL is on file in English only" does not go in.
2. **HELD on wording too, question 1.** (a) Provider outage, ruled text: "when the model provider is unavailable the prototype retries and stops; the gates run without the model; no one is handed the conversation; gap 1's recommendation is the mechanism". Source cited by the ruling: pack page 6; main differs, `onyx/coordinator.py` 219 to 233.
3. (b) Authorship: "the scenarios, the gates and the answer keys were written by the same team; the keys were frozen after a blind review in which 27 of 28 verdicts agreed (archive 2026-10-21); the recall figures measure agreement with keys the team wrote". Source: `onyx-hackathon-build-archive.md` line 46.
4. (c) Log and erasure: "an append-only hash-chained log that holds personal data collides with the PDPL right to erasure; the answer, identifiers out of the chain and in a separately erasable store, is not built". Source: Ra'ed's answer 12; `onyx/audit.py`.
5. (d) De-identification: "the transfer gate checks field names, not content; the subscriber's question left verbatim under the label 'de-identified'; free text can re-identify; the label is a design rule, not a tested control". Source: `onyx/gate.py` 417 to 465; `runs/c5/S3/run1.jsonl`, "question text (Hind's question, verbatim)".
6. (e) Objection: "the objection received at step 1 is read by the sharing and marketing gates from the account record; the transfer gate does not read it, and the prototype does not write the step 1 objection into the record". Source: `onyx/data/scenarios/S3.json` account; `onyx/gate.py` 404, 583.
7. (f) `docs/report.md` line 159: "a data-protection practitioner's review of the gates' law" becomes "a data-protection practitioner's review (practice, not legal advice)". Source: docx, "What this is not". This one sentence does not grow the page.

### 51.J Reviewer credit (ruling 3)

Exactly: "Ra'ed Shraim, Director Business Excellence – DPO, Solidarity First Insurance Company, Amman – Jordan", with "practitioner review, not legal advice, no UAE standing" beside it. In the README team table of 51.D as a reviewer row; the written yes that 51.D waits for now exists. Source: `D:\Downloads\Mizan-Review-Response-2026-11-05.docx`, lines 35 to 37 of its text.

### 51.K Register rows and rule notes (ruling 3)

Edit `onyx/data/gaps.json` and `onyx/gaps.py`, regenerate.

1. **HELD, question 5.** Licence 9.1: complete the Arabic quote from the licence text. Source: `standards-text/licence-2-2026-etisalat-public-telecom-en-ar.txt` line 947 onward, PDF page 22; Iyas eye-checks block 90 first. The rule's `quote_ar` and the chunk cannot take it.
2. Licence 3.4.1, rule note in `rules.json`: add that subcontracting needs TDRA's prior written approval, the half the gate does not cite. Source: chunk `licence-2-2026:3.4.1`.
3. Gap 1: add the sourced tension, licence 9.1 "promptly" against Trade Law 14/2023 Art 6(7) "always available without interruption with qualified staff". Add to the recommendation, marked inferred: "the agent stops the conversation; a system acknowledgement carrying the 26.13.2 reference number is not a conversation". Sources: chunks `licence-2-2026:9.1`, `law-14-2023-en:6(7)` p. 9, `tdra-cpr-v2-en:26.13.2`. Question 5 asks whether the Arabic "دون إبطاء" goes beside "promptly".
4. Gap 3 recommendation: map trust levels to acts, not channels; a protective reversible act (block a line reported lost) needs a lower level than an irreversible one (unblock, port, SIM replacement); log failed attempts. In our words. Sources: ET 33(1), eIDAS 8(3)(c), both already in the row; Ra'ed's answer 9.
5. Gap 5 and gap 9: one line each, "Interim position (practitioner's view, reviewer)", compressed from his answers 2 and 5, attributed to him. No other row. Gap 9's line must not imply `minor_signal` exists: it is not built. The row has no such field; `onyx/gaps.py` and the site gain one.
6. Gap 2: one sentence only, that the CPR classifies by sales medium and the PDPL by processing purpose, and no text requires a conversational channel to elicit and store the two consents separately. The row is not reframed. Source: ruling 3; Ra'ed's answer 4.

### Not adopted before 11-09 (ruling 3; the reasons are there)

Re-ordering gap rows by evidential strength. Any gate change (objection register, re-identification test, `minor_signal` hold, fail-closed proof, chapeau-aware check text). Dialect rewrites of the S2 Arabic lines. His clocks (two minutes, one business day, 10/20 days). The provider contract clause list and go-live checklist.

### Stop and ask, added

A held item is reached with no answer on file. A chapeau rule row needs a chunk file touched. A quote cannot be found on the source page. Iyas's wrong-translation list names a quote in a frozen key. Before the PDF leaves, re-run the Arabic rendering check of ruling 2.2 on the rebuilt `docs/report.pdf` and paste the output in the report-back.
