# Ruling on the six fit-check questions, and the 90-pair read (Fable, 2026-11-05, about 22:00 Amman)

Answers `D:\Projects\engineering\onyx-hackathon-build\docs\report-back\2026-11-05-raed-ruling-fit-check.md`.
Read against main 7de5b3f and task-50 at 8168d48. Supersedes the Ra'ed ruling
(`raed-review-ruling-2026-11-05-fable.md`) wherever the two differ: the fit check showed that ruling
stated facts that are false on main.

## The six questions

**1. Outage sentence.** The build's wording is accepted as written: "When the model provider is
unavailable the prototype retries, then writes a plain-code hand-over to the named human and the gate
decides it; the gates run without the model. This is shown by fault injection on a replay; no live
outage was run and no real human queue or subscriber notice exists. Gap 1's recommendation is the
mechanism." Ruling 3 (a) is withdrawn.

**2. Arabic coverage paragraph.** The build's paragraph is accepted with one correction. "gaps 2, 4, 5,
6 and 7 rest on the English text" is wrong for gap 2, which quotes nine CPR clauses in Arabic (eye-check
blocks 21 to 29). Write: "... so the replay pages print 'no Arabic text on file' for PDPL clauses, and
gaps 2, 4, 5, 6 and 7 rest on the English text for the PDPL clauses they cite." Ruling 2.1's paragraph
is withdrawn.

**3. Limits length.** The build's split is accepted: Limits in the body is two sentences naming the
limits plus a pointer to Annex A; the full text goes under a new bold lead in Annex A; the 26.7.2
four-clause note goes in gap 1 of the register, Annex B under the rule sample, and Annex C, not in the
body. Page 5 keeps its last sentence. No cut in the body. After the Word build, count the pages: if the
main text runs past 5, cut the Limits body to one sentence plus the pointer; if it still runs past 5,
stop and ask hq with the overflow measured in lines.

**4. Chapeau row.** No row. 109 stays everywhere. The chapeau is quoted in prose in gap 1 and the annex,
in both languages, after Iyas passes block 89. No chunk file is touched.

**5. Licence 9.1.** Rule and chunk stay as they are. The gap-1 9.1 entry gets `quote_ar` and `file_ar`
from a new checked file under `docs/sources/`, made only after Iyas passes block 90 (see the read below:
the last sentence may be missing a word). Allowed files widen by that one file. The gap-1 tension row
quotes both languages, Arabic first because licence 16.7 makes it binding: «دون إبطاء» (without delay;
the English text reads "promptly").

**6.1 Gap 15, block 66.** Confirmed wrong: the English is the Cabinet sentence of 79 bis (2), the Arabic
is the Board sentence. Fix in Task 51: the Arabic Cabinet sentence from the top of PDF page 24 of
`telecom-law-3-2003-ar.pdf`. The text layer is broken there, so the build transcribes it from the page
image, puts it on one eye-check block (text, where line, link, page image), and Iyas passes it before it
lands in `gaps.json`. It is a `quote_ar` wording change, in scope. Nothing in a frozen key quotes it.

**6.2 Footer run-ins (26.6, 4.23.2, 24.6).** The three `quote_ar` strings in `gaps.json` end with the
printed footer, and 4.23.2 and 24.6 also carry footnote text (3 and 35); the site shows it all. If the build can end each string at the clause's own full stop by
editing `gaps.json` only, with the chunk untouched, `onyx/data.py` 88 still satisfied (a shorter string is
still verbatim in the chunk) and every test green, do it in Task 51. If it needs a chunk edit, after the
shortlist, on that list.

## The 90 pairs, read by Fable

Read from the page's text, not the page images. This read says whether the English says what the Arabic
says. It does not say the Arabic is on the page: the script said that for 76 blocks, and 3 blocks nobody
has yet read on the page. Claude Cowork read the same 90 separately (Iyas, 2026-11-05): same wrong block,
same three by-eye blocks, same divergences; its two additions (48, footnotes in 29 and 36) are merged here.

**Wrong (1):** block 66, as above.

**Iyas reads these on the page (5):**
- 34 (Decision 16/2026 4.17): the PDF is a scan, no script could find it. Is the sentence on page 10?
- 65 and 66 (Telecom Law 79 bis, page 23): broken text layer. Is 65 on the page as written? For 66, read
  the top of page 24 and say whether the Cabinet sentence is there.
- 89 (CPR 26.7 chapeau, page 51): Task 51 quotes it. Four words, one look.
- 90 (licence 9.1 full, page 22): the stored Arabic ends «...المبالغ المستحقة للمشتركين وبشكل كامل». The
  stray «و» before «بشكل كامل» suggests a dropped word (the English has "promptly and in full"). Does the
  page have a word between «للمشتركين» and «وبشكل كامل»? If yes, which?

**Source divergences, no change (noted so nobody "fixes" them):**
- 1 and 15: Arabic says days, English says calendar days (already on file).
- 33 (CPR 20.11.1): Arabic «الأسئلة التعريفية» (identification questions), English "security questions".
- 37 (CPR 3.3): English "transparency and fairness", Arabic as held has «بشفافية» only. Either the
  Arabic text omits fairness or the stored chunk lost a word. The register line says "transparency"
  only, so nothing printed is wrong. Check after the shortlist.
- 57 (PDPL 9(1)): Arabic «ونتائج التحقيق» (results of the investigation), official English "investigation
  rights". The official English is what it is; our quoted part matches.
- 48 (CPR 17.3): Arabic «صحف محلية» (local newspapers), English "national newspapers". The law's own
  wording in each language; quote each as printed.
- 49 (CPR 26.6): "personal" for "personnel" is the official English text's typo. Quote as printed.
- 68 (CPR 4.4): «تجدديها» is the source's own misspelling.
- 72 (S2 step 3): Arabic «محتوى مدفوع» (paid content) for "premium content". Same meaning, keep.

**Everything else (81 blocks):** the English says what the Arabic says. The S2 lines (69 to 75) are
good Modern Standard Arabic and match their English; step 1's Arabic spells out "twice: once under sales
rules, once under complaint rules", which is what the English means.

## Order to the build (Opus)

**Changed 2026-11-05 (Iyas): one task per session. The session that finishes Task 50 stops at its report-back and does not start Task 51. Task 51 starts in a fresh session after hq merges Task 50, and the items below apply to it there.**

1. If Task 50's stop-1 ruling is not yet applied, apply it first:
   `D:\Projects\hq\uni\ai-for-good-hackathon\task-50-stop-1-ruling-2026-11-05.md`. Then the Task 50
   report-back, then hq checks and merges.
2. The six HELD items in `task-50-51-order-2026-11-05.md` are released with the answers above. Items 4, 5
   and 6.1 wait for Iyas's word on blocks 89, 90 and 66; build everything else first.
3. Block 66's replacement sentence gets its own eye-check block before it enters `gaps.json`.
4. Report-back lists, for each of the six, the file and line changed, and the page count after the Word build.
5. Stop and ask when: a frozen key would change; the page count stays over 5 after the Limits cut; the
   footer trim needs a chunk edit.
