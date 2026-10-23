# Order: Task 20, gap-10 (Arabic at equal quality on an automated channel) (hq, Fable, 2026-10-24)

Build model: Opus 5.5. No model calls; USD 0. Copy this file into `docs/work-orders/` first. Gate, `rules.json`, keys,
mandates, scorer, chunks already committed and every recorded run stay byte-identical, as in Tasks 15 and 19.

Decision (hq, Fable, 2026-10-24, KB searched in both languages, every text on disk grepped for Arabic / English /
language / اللغة / لغة): the candidate becomes **gap-10**. The UAE texts say *which* language a consumer is served in
and fine the omission of Arabic; no text says that an automated channel must perform as well in Arabic as in English,
or that quality is measured per language. The duty exists, the method does not: kind **method**, category **standards
gap**, addressee **TDRA** (the QoS Policy is the instrument that measures service quality and has no per-language
indicator). Exposed by our own C5 scoring per language, the only such measurement in the field.

## Sources allowed, and nothing else

- `kb/chunks/`: `tdra-cpr-v2-en:3.2.2` (p. 10, EN and AR in the chunk); `consumer-law-15-2020-en:8(4)` (p. 6);
  `cabinet-66-2023-en:43(5)` (p. 24, Annex 2 rows for Art 8(4) and Art 26); `qos-v3-en` (all rows: searched, silent).
- `kb/chunks-full/`: `tdra-cpr-v2-en:4.25.3` (p. 19), `tdra-cpr-v2-en:17.3` (p. 51), `consumer-law-15-2020-en:25(1)`
  (p. 10), `consumer-law-15-2020-en:26` (p. 10), `licence-2-2026:16.7` (p. 47). These five lines move into
  `kb/chunks/` the way Task 15 added four (append; no existing line changed; no full rebuild).
- Readiness 2.0 (`kb/sources/global/` has none; hq file `standards-text/itu-ai-readiness-report-2-0-2026-01.txt`,
  already the source of `itu-readiness-dimensions.json`): dimension 6 Human Interface metric "Availability of AI
  models in the local language used in the human interface" (p. 23 of the report). Framework row, non-binding.
- One fetch, below. Nothing else is fetched; if it fails, stop and ask.

## Items

1. **One fetch, global example:** Canada's Official Languages Act, R.S.C. 1985, c. 31 (4th Supp.), Part IV, from
   laws-lois.justice.gc.ca only (pages `eng/acts/O-3.01/page-2.html` and `page-3.html`, or the full text page), saved
   as `kb/sources/global/canada-ola-part-iv.txt` with URL, fetch date and section text only, the same shape as
   `coppa-16cfr312-5.txt`. hq opened both pages on 2026-10-24 and the quotes below are from them; verify verbatim
   against the fetched text as Task 9 did.
   - s. 22: "Every federal institution has the duty to ensure that any member of the public can communicate with and
     obtain available services from its head or central office in either official language"
   - s. 26: "Every federal institution that regulates persons or organizations with respect to any of their activities
     that relate to the health, safety or security of members of the public has the duty to ensure, through its
     regulation of those persons or organizations, wherever it is reasonable to do so in the circumstances, that
     members of the public can communicate with and obtain available services from those persons or organizations
     in relation to those activities in both official languages."
   - s. 27: "the duty applies in respect of oral and written communications and in respect of any documents or
     activities that relate to those communications or services."
   Why these three: 22 is the service duty, 27 extends it to oral (so to a chat or voice agent), 26 is a regulator's
   duty to impose it through regulation, the shape of what we ask TDRA. The Act, like the UAE texts, sets the language
   and not a quality measure; the register says so (no instrument we hold measures parity; the recommendation is ours).

2. **Row gap-10** in `onyx/data/gaps.json`, generated into `docs/gaps.md` and the README register:
   - `line`: "Arabic at equal quality".
   - `gap`: "Arabic on an automated channel: the texts set the language (CPR 3.2.2: written information in Arabic or
     English as the Consumer prefers, both if unknown; Consumer Law 26: data, advertisements and contracts in Arabic;
     8(4): the invoice in Arabic; Cabinet 66/2023 Annex 2: AED 100,000 for each) and none sets the quality: no binding
     text requires an automated channel to answer as well in Arabic as in English, and the QoS Policy v3.0 has no
     indicator per language."
   - `kind` method; `category` standards gap; `addressee` TDRA; `global example` "Canada OLA s. 22; s. 26; s. 27";
     `exposed by` "C5 per-language scoring (M, D nodes); mapping (SRC)".
   - Searched rows, one line each of what the clause says, Arabic where the chunk holds it:
     `tdra-cpr-v2-en:3.2.2` (language of written information, by preference; both if unknown; 3.2.1 allows electronic
     form, so an app chat is inside it: inferred, say so); `tdra-cpr-v2-en:4.25.3` (PSCM "in the appropriate
     language": RBT only); `tdra-cpr-v2-en:17.3` (price-rise notice: three Arabic and two English newspapers);
     `consumer-law-15-2020-en:26` (Arabic for consumer data, advertisements, contracts; other languages in addition);
     `consumer-law-15-2020-en:25(1)` (e-commerce: "adequate information in Arabic"); `consumer-law-15-2020-en:8(4)`
     (invoice in Arabic); `cabinet-66-2023-en:43(5)` (Annex 2: AED 100,000, Art 8(4); AED 100,000, Art 26);
     `licence-2-2026:16.7` (the licence's Arabic version binds: a document rule, not a service rule); `qos-v3-en`
     (every T indicator; none distinguishes language). Add the Readiness 2.0 dimension 6 metric as a framework line,
     marked non-binding.
   - `uae_position`: "The language duty is binding and fined; Mizan meets it by answering in the subscriber's language
     with the clause quoted in that language. Nothing says the Arabic answer must be as good as the English one, and
     nothing measures it: the QoS Policy counts waits and faults, not languages. Mizan's own figures show the gap can
     be measured: action recall 0.96 English and 0.94 Arabic, citation validity 0.99 and 1.00 (C5, two runs per
     scenario per language); the Arabic S2 run cites the Arabic chunk ids. Searched 2026-10-24 in both languages."
   - `recommendation`: "TDRA to add to the QoS Policy, for every automated consumer channel, the same indicators per
     language (answer accuracy against the Licensee's own policy text, hand-over time, abstention), reported
     separately for Arabic and English, with a parity band; Canada's Official Languages Act s. 26 shows a regulator
     imposing the language duty on regulated service providers, and s. 27 extends it to oral channels."
   - `competitor`: "no"; `competitor_basis`: "another team's gap table has no language row; another team's GAP-06 asks the same
     question for Cameroon's two official languages (reading note), which is why the candidate was searched."
   - The existing candidate "Arabic records" stays as it is (invoices and records; a different question).

3. **Report and README.** The gap count moves from nine to ten wherever a count appears (README, `docs/report.md`,
   judge card if present); one sentence in the report's gaps paragraph: "Gap 10: the texts fix the language of
   service and fine its omission; none fixes its quality per language, which our per-language figures show is
   measurable." Re-render `report.docx`; the five pages hold (Task 18 ladder: if page six appears, apply its next
   step, not a new cut). Figures unchanged.

4. **Checks** (all run, output in the report-back): `python -m onyx gaps` regenerates with no diff beyond the new row
   and counts; the five new chunk lines appear once each in `kb/chunks/` and no existing line changed (`git diff
   --stat` on the chunk files shows additions only); the three Canadian quotes verified against the fetched file;
   `git diff <Task 19b commit>..HEAD -- onyx/gate.py onyx/data/rules.json onyx/data/keys onyx/data/mandates.json
   onyx/scorer.py runs/` prints nothing; full suite; check-data; CI green; Word page count printed.

Stop and ask if: the fetch fails; a searched chunk says something other than this order claims; the report goes to
six pages after one ladder step; anything needs a model call or a change beyond the files named here.

Report in under 25 lines, with commit hashes and one line per check.
