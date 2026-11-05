# Ra'ed ruling, section 5: rendering check, fit check, stop (Opus, 2026-11-05)

For hq, on Fable. Answers `D:\Projects\hq\uni\ai-for-good-hackathon\raed-review-ruling-2026-11-05-fable.md` section 5 (sha256 `efc755c1...748a65f`). Read against main at 7de5b3f. No repo code changed. Items 5.1 and 5.3 are done. Item 5.2 is appended with the six items below marked HELD. A held item is not built until hq answers.

## Questions for hq

Each one is wording a ruling fixed, or a stop the ruling names. The build does not re-decide them. Recommendations are the build's and are not rulings.

### 1. Limits (a), the outage sentence, is false on main

Ruling 3 (a): "the prototype retries and stops; the gates run without the model; no one is handed the conversation". It cites pack page 6, dated 2026-10-25. Task 29 Part A came after that.

- `onyx/coordinator.py` 149 and 219 to 233: after the last retry it logs `model_unavailable`, writes a plain-code `escalate_to_human` to the named human, the gate decides it, and the run continues.
- `docs/report.md` line 104: "the coordinator's deny-by-default hold hands the conversation to the same human, with no model in that step". README line 60 says the same.

The report would contradict itself. What stays true: this is shown only by fault injection in a replay, and no real queue, human or subscriber notice exists.

Recommended: "When the model provider is unavailable the prototype retries, then writes a plain-code hand-over to the named human and the gate decides it; the gates run without the model. This is shown by fault injection on a replay; no live outage was run and no real human queue or subscriber notice exists. Gap 1's recommendation is the mechanism."

### 2. The Arabic coverage paragraph (ruling 2.1) has three wrong facts

| Ruling says | Main says | Evidence |
|---|---|---|
| "The CPR, the licence and TDRA Decision 16/2026 are chunked in both languages" | True for the CPR only. Licence: 9 chunks, 1 with Arabic, the checked 9.1 fragment. Decision 16: 2 chunks, Arabic only, no English | count over `kb/chunks/*.jsonl`: CPR 71 en / 71 ar; licence 9 / 1; decision-16 0 / 2; PDPL 24 / 0 |
| "the recorded runs log 'no Arabic text on file'" | The logs do not hold that phrase. The replay pages print it | `git grep` over `runs/`: 0 files; `onyx/replay_page.py` 120; `docs/replay/S3.md` 10 hits, `S4.md` 21 |
| "gaps 2, 4 and 5 rest on the English text" | True, but gaps 6 and 7 also cite one PDPL clause each with no Arabic | `onyx/data/gaps.json`: gap-2 2, gap-4 8, gap-5 8, gap-6 1, gap-7 1 |

The ruling's fact line "gap-5 quotes it twice" is also off: the PDPL Arabic quotes sit in gaps 13 and 14, four lines each (`docs/gaps.md` 766 to 777 and 799 to 808). Gap 5 has none.

Recommended: "Arabic coverage is uneven. Every CPR clause held is chunked in both languages; TDRA Decision 16/2026 is held in Arabic only; of the licence, only a checked fragment of 9.1 is chunked in Arabic. The PDPL Arabic is on file and quoted in gaps 13 and 14 but not chunked, so the replay pages print 'no Arabic text on file' for PDPL clauses and gaps 2, 4, 5, 6 and 7 rest on the English text. The Arabic scenario lines are written in Modern Standard Arabic; dialect handling is untested."

### 3. The Limits additions do not fit in 5 pages

`docs/report.pdf`: last ink on page 4 at y 719.0, on page 5 at y 717.6, with the text bottom at 720 if the margin is one inch (assumed). No free line on either page. Ruling 2.1 and 3 (a) to (e) add about 240 words to a section that is now 3 lines, and 51.B and 51.C already compete for the same space. Order stop: "The main text leaves 5 pages". The ruling names no cut. The full 26.7.2 note (ruling 1.3: four clauses in two languages plus about 75 words) has the same problem if "the S2 hand-over narrative" means `docs/report.md` lines 100 to 104.

Recommended: Limits gets two sentences naming the limits, plus a pointer. The full text goes under a new bold lead in Annex A. Page 5 keeps its last sentence. The 26.7.2 note goes in gap 1 of the register, Annex B under the rule sample, and Annex C, and not in the report body. The alternative is that hq names a cut in the body. Not measured: the real page count, which needs the Word build.

### 4. The chapeau rule row needs a chunk file (ruling 1.4, stop 5.4)

`kb/chunks/tdra-cpr-v2-en.jsonl` has 26.6, 26.7.1 and 26.7.2 but no 26.7. It is only in `kb/chunks-full/`. `onyx/data.py` 77 to 79 fails a rule with no chunk, and a `searched` entry in gaps.json needs one too unless it names a stored file (`data.py` 44 to 47). A chunk change also trips `StaleMeasurement` and breaks the order's limit. Adding a row would move 109 at `docs/annex.md` 50 and 151 and `tests/test_whatif.py` 25.

Recommended: no row. 109 stays. Quote the chapeau in prose in gap 1 and the annex. Iyas checks the words at block 89 of the eye-check page.

### 5. Licence 9.1, "complete the Arabic quote": the rule and chunk cannot take it

`rules.json` `quote_ar` must sit verbatim in the chunk's `text_ar` (`onyx/data.py` 88), and the chunk holds only the fragment. `tests/test_data.py` 105 pins the fragment. `onyx/gate.py` 119 copies `quote_ar` into every gate reason, so changing it separates rules.json from what the recorded logs hold.

Recommended: rule and chunk stay. The gap-1 9.1 entry gets `quote_ar` and `file_ar` (`onyx/gaps.py` 167 prints it), from a new checked file under `docs/sources/`, after Iyas passes block 90. Allowed files widen by that one file.

Also for hq: the binding Arabic of 9.1 says "دون إبطاء" (without delay). The ruling's gap-1 tension quotes the English "promptly". Should the row quote both?

### 6. Found by the eye-check build, not in the ruling

1. Gap 15, `docs/gaps.md` 834 to 835: the English quote is the Cabinet sentence of 79 bis (2), the Arabic beside it is the Board sentence. They are not translations of each other. The Arabic Cabinet sentence is at the top of PDF page 24 of `telecom-law-3-2003-ar.pdf`. Flagged on block 66. Fixing it is a `quote_ar` wording change, in scope. Recommended: add the Cabinet sentence to Task 51 after Iyas reads it, because that page's text layer is broken.
2. The stored Arabic of CPR 26.6, 4.23.2 and 24.6 runs into the printed page footer ("صفحة51", "الإصدار 25 يوليو 2023م"), and `docs/site/gaps.html` prints it. The fix is a chunk edit. Recommended: leave until after the shortlist, and add it to that list.

## What the fit check passed

| Ruling item | Check | Result |
|---|---|---|
| 1.5 | `git grep -i prevail` over README, report, annex, onyx, tests | No claim about the CPR or a gate table. Only portal laws: rules on `pdpl-45-2021-en` and `telecom-law-3-2003-en`, README 32, annex 338, gaps.json 353, 354, 623. Nothing to correct on main; Task 51 confirms by grep |
| 3 (b) | Archive | "27 of 28" at `onyx-hackathon-build-archive.md` 46 |
| 3 (d) | `onyx/gate.py` 417 to 465; `runs/c5/S3/run1.jsonl` | Gate reads `DIRECT_IDENTIFIERS` terms in the payload; log: "question text (Hind's question, verbatim), plan name" |
| 3 (e) | `S3.json`; `gate.py` 404, 583 | Sharing and marketing gates read `marketing_opt_out`; the provider gate does not; the account's opt-out is dated 2026-03-02, not written at step 1 |
| 3 (f) | `docs/report.md` 159 to 160 | String present |
| Credit | Docx lines 3, 35 to 37 | Exact title given, "I agree to be named"; his qualification (no standing under UAE law) matches the ruling's words |
| Licence 3.4.1 | Chunk | "with the prior writ..." present |
| Gap 1 | `law-14-2023-en` 6(7) p. 9; `kb/sources/law-14-2023-en.txt` 256 | "always available without interruption with qualified staff" |
| Gap 3 | gaps.json gap-3 | ET 33(1) and eIDAS 8(3)(c) are in the row |
| Gaps 5, 9 | Docx answers 2 and 5 | Those answers are those gaps. Gap 9's answer also proposes `minor_signal`, which is not built, so the interim line must not imply it is |
| Order fit | Task 51 Done means 7 | `onyx/data/rules.json` was not allowed; the appended section adds it for the `language_note` of cpr-26-7-2 and the note of licence-3-4-1 only |
| Order fit | 51.D "no reviewer line" | That line waits on a written yes, which now exists; the appended section adds the row |

## Rendering check (ruling 2.2)

Script: per PDF page, Arabic characters, the fonts carrying them, and glyph ids. Glyph id 0 is the empty box. Site pages were printed through headless Chrome on this PC.

Control, the pack sent to Ra'ed, so the test can fail:

```
mizan-review-raed-shraim-2026-10-25.pdf  pages 18
p7:  arabic_chars=402 notdef_arabic=0   arabic_fonts={'ArialMT': 402}
p13: arabic_chars=103 notdef_arabic=103 arabic_fonts={'Calibri-Italic': 103} distinct_glyphs=1
p18: arabic_chars=36  notdef_arabic=0   arabic_fonts={'Calibri': 36}
FAIL pages: [13]
```

Page 13 is TDRA Decision 16/2026 4.17 in gap 3. I looked at the render and it is the row of empty boxes he reported.

Current files:

```
docs/report.pdf  pages 12
p8: arabic_chars=57 notdef_arabic=0 arabic_fonts={'CourierNewPSMT': 57} distinct_glyphs=28
FAIL pages: []

file             pages  pages with Arabic  notdef  Arabic fonts
site/index           3                  0       0  none
site/gaps           55                 36       0  SegoeUI
site/kb             23                  6       0  SegoeUI
site/runs            2                  1       0  SegoeUI, SegoeUI-Bold (as it loads)
site/runs, all      48                 31       0  SegoeUI, SegoeUI-Bold (every step of every run forced visible, in a scratch copy)
site/verify          1                  0       0  none at load
site/whatif          3                  1       0  SegoeUI
site/modeldown       2                  0       0  none
site/localmodel      3                  0       0  none
```

Corrupted text in `docs/site/*.html`, `docs/gaps.md`, `docs/report.md`, `docs/annex.md`, `README.md`: U+FFFD 0, "???" 0, "؟؟؟" 0, broken encoding 0, private-use characters 0.

Looked at by eye: report page 8 whole and zoomed (Arabic reads correctly, joined, in Courier New, thin and letter-spaced but legible); up to 3 Arabic lines per page for every Arabic page of all the files above, on nine contact sheets. All show Arabic letters.

Not covered:

- The glyph check covers every character, but the eye saw a sample of lines, not every line.
- Site fonts come from the reader's machine: tested on this Windows PC only (Segoe UI). The CSS falls back to Geeza Pro, Noto Naskh and others; no Mac or phone was tried.
- `verify.html` holds 457,212 Arabic characters in embedded log data and draws none at load. Its check run was not exercised.
- `docs/report.pdf` is main's; Task 51 rebuilds it, so re-run this on the new PDF before it leaves.

## Eye-check page (ruling 2.3)

`D:\Projects\hq\uni\ai-for-good-hackathon\arabic-eye-check-2026-11-05.html`, images in the `-pages` folder beside it. Private, not published, opened in Chrome. 90 blocks:

- A: 3 rules.
- B: 65 blocks covering all 72 AR lines; 7 lines repeat word for word and share a block that lists each line.
- C: S2 title and 6 steps.
- D: 2 annex lines.
- E: 11 pieces of Arabic inside English lines (added: Iyas asked for every pair).
- F: 2 for Task 51 (26.7 chapeau, licence 9.1 full).

Where the script found the Arabic:

| Result | Blocks |
|---|---|
| In the PDF, word for word | 57, plus the 2 F blocks (read by hand from the same text) |
| In a text file, word for word | 11 |
| In the PDF, most words (footers break the rest) | 4 |
| By eye: the PDF's text layer is broken (79 bis, page 23) | 2 |
| By eye: the PDF is a scan (Decision 16, page 10) | 1 |
| No source page: team text, portal screen, search term | 13 |

No quote was missing from its source. Not done by the script: it confirms the Arabic is on the page. It does not judge a translation. That is Iyas's check.
