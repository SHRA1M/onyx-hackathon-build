# Report-back: Task 56b, the site's look (2026-11-08, Opus)

Order: `docs/work-orders/2026-11-08-task-56b-site-look.md` (copy of `D:\Projects\hq\uni\ai-for-good-hackathon\task-56b-site-colours-font-width-order-2026-11-08.md`). Branch `task-56`, commits added to PR #26, not merged. No model call.

## In plain words

The site now wears DP Technologies' Vault colours: a full-width navy bar with white links, the current page in gold, warm off-white page, white cards, navy headings. It uses IBM Plex (Sans, Sans Arabic, Mono), stored inside the site so it works offline. Pages use the full window up to 1440 px; running paragraphs stay near 80 characters. The knowledge base shows "Arabic", "English", not "ar", "en". Each scenario on the runs page now reads as a chat: the message on one side, the agent's proposal on the other, the code's answer as a coloured label, the clauses in a fold.

## What was built

1. Colours (item 1), in `onyx/site.py` `SITE_CSS`: the five Vault values as oklch, with hex fallbacks first (computed from the oklch values): navy `#172846`, gold `#f1a716`, page `#f8f6f4`, panel `#ffffff`, text `#151b24`. Table heads navy. Hold changed to amber-brown `#914f2f` / `oklch(0.5 0.1 45)`, clearly apart from the gold; allow green and block red unchanged. Dark mode: navy background `oklch(0.2 0.04 260)`, same gold. Links are a darker blue `#1d4f91` in light mode (gold text on white fails contrast), gold in dark mode.
2. Font (item 2): `docs/site/fonts/`, 7 woff2 files plus `OFL.txt`, **468,896 bytes** total (under 1.5 MB). Source: npm `@ibm/plex-sans` 1.1.0, `@ibm/plex-sans-arabic` 1.1.0, `@ibm/plex-mono` 2.5.0 (the official IBM packages), `fonts/complete/woff2/`. Sans and Sans Arabic in regular, semibold, bold; Mono regular. The three packages' LICENSE.txt files are byte-identical (SIL OFL 1.1, "Copyright 2017 IBM Corp. with Reserved Font Name Plex"); one copy is `OFL.txt`. Loaded by `@font-face` with relative paths; system fonts stay as fallbacks.
3. Width (item 3): the 992 px body cap is gone. Content is `max-width: 1440px` with a 32 px gutter (16 px at 700 px and below), on the site pages and on the runs page's header and main. Paragraphs, notices and meta lines cap at 80ch; tables, cards and the runs chat use the full width; overview cards fill the row.
4. Language names (item 4): `site.language_name` maps `ar, de, en, es` (and `fr`) to names; `en,ar` shows "English, Arabic". Used for the knowledge-base language filter buttons and the language column. `data-value` and `data-language` keep the codes.
5. Runs as a chat (item 5), in `onyx/replay_viewer.py`:
   - The release message in a bubble on the start side, labelled from the scenario step's `from`: subscriber is "Customer"; coordinator "Coordinator"; human "Staff member"; tdra "TDRA"; partner "Partner"; system "System".
   - Each `propose` event a bubble on the end side, labelled by its logged actor: care "Care agent", adviser "Adviser", data_office "Data office", tdra "TDRA". `classify_channel` (the log marks it plain code) is labelled "plain code".
   - Each gate event: a coloured label (Allowed green, Held for a staff member amber-brown, Blocked red, Not enough evidence grey), beside a fold whose summary is the old line "Gate on <verb>: <verdict>" word for word, with the clauses and quotes inside.
   - Hand-over box headed "Handed to staff member", clauses and quotes as before.
   - "Without the gates" stays a fold under the step. Hold notes, override notes and the abstain box stay.
   - Scenario picker: one card per scenario (id over the English title; the Arabic title replaces it in the Arabic view). The what-if and model-down entries are cards too.
   - Arabic view: the chat is `dir="rtl"`, so the sides mirror; the English proposal lines and the folds inside it stay left to right so their punctuation reads correctly.
   - English/Arabic, Previous/Next and Present unchanged (JS only adds a `lang-ar` body class for the picker titles).
   - `CHAT_CSS` lives in the viewer, so `docs/replay/index.html` gets the same layout (in html_kit's colours). `onyx/html_kit.py` not touched.
6. Tests: two pins on the picker button markup moved to `class="pick"` (`tests/test_modeldown.py`, `tests/test_whatif.py`). No figure pin changed.

## Differs from the order, and why

- The old step heading "Step N of T: from X to Y" is kept as a small grey line above each chat, so its words stay on the page.
- The run header's meta line still ends "..., en;" / "..., ar;": it is inside a sentence, which this order keeps word for word. The gap register's "EN:" / "AR:" prefixes before quotes are kept for the same reason. hq to say if Task 56c should change them.
- No `CHANGELOG.md` entry: not in the order's file list (same open question as Task 56).
- Screenshots are one window high (1080, 900, 844), not full page; at 390 the runs shots start at the step.

## Checks (done means)

### 1. Tests and selftest

`uv run pytest -q`:

```
1178 passed in 379.50s (0:06:19)
```

`python -m onyx selftest`:

```
figures match a fresh eval of runs/
selftest exit 0
```

### 2. Files changed

```
 docs/replay/index.html           | 629 +++++++++++++++++++++------------
 docs/site/gaps.html              | 117 ++++--
 docs/site/index.html             | 117 ++++--
 docs/site/kb.html                | 119 +++++--
 docs/site/localmodel.html        | 117 ++++--
 docs/site/modeldown.html         | 117 ++++--
 docs/site/runs.html              | 746 +++++++++++++++++++++++++--------------
 docs/site/screenshots/index.png  | Bin 116449 -> 106015 bytes
 docs/site/screenshots/verify.png | Bin 110348 -> 44784 bytes
 docs/site/verify.html            | 117 ++++--
 docs/site/whatif.html            | 117 ++++--
 onyx/replay_viewer.py            | 110 ++++--
 onyx/site.py                     | 140 +++++---
 tests/test_modeldown.py          |   4 +-
 tests/test_whatif.py             |   2 +-
```

New: `docs/site/fonts/` (8 files), `docs/report-back/task-56b-shots/` (24 files), the order copy, this file. `git diff --stat -- 'docs/replay/*.md'`: empty.

### 3. Visible words, old against new (word counts, scripts and styles stripped, folds included)

```
gaps.html, index.html, localmodel.html, modeldown.html, verify.html, whatif.html: lost 0 words, added 0
kb.html: LOST ar 27, de 2, en 78, en,ar 4, es 2
         ADDED Arabic 31, German 2, English 78, English, 4, Spanish 2
runs.html and docs/replay/index.html: LOST Proposals 56, Gate 56, human 2
         ADDED the labels below
```

Nothing but labels lost: "Proposals" and "Gate" were the two step sub-headings; "human" was in "Handed to a human". Every "Gate on <verb>: <verdict>" line, clause, quote, figure and sentence is still on the page.

Labels added or changed (the only new words):

| Old | New |
|---|---|
| (none) | Customer, Coordinator, Staff member, TDRA, Partner, System (sender labels) |
| (none) | Care agent, Adviser, Data office, TDRA, plain code (proposal labels) |
| (none) | Allowed, Held for a staff member, Blocked, Not enough evidence (answer labels) |
| h4 "Proposals", h4 "Gate" | removed (the chat shows both) |
| Handed to a human | Handed to staff member |
| ar, en, de, es, en,ar (kb) | Arabic, English, German, Spanish, English, Arabic |

### 4. Screenshots

`docs/report-back/task-56b-shots/`: `index-`, `kb-`, `runs-S2-step3-en-`, `runs-S2-step3-ar-` at `1920`, `1280`, `390`, each `light` and `dark` (24 files). Retaken: `docs/site/screenshots/index.png` (1280x1400), `verify.png` (1280x900). Taken with Playwright 1.57 on the installed Chromium, from `file://`.

### 5. Font and sideways scroll (from `file://`, every page, 1920/1280/390, light and dark)

All 48 page loads printed `sideways overflow 0px, Plex Sans loaded True` (`document.fonts.check('16px "IBM Plex Sans"')`), and the runs page at S2 step 3 showed `Step 3 of 6, overflow 0px` in English and Arabic at every width.

## Open questions for hq

1. Should Task 56c turn the meta line's "en"/"ar" and the gap register's "EN:"/"AR:" into names? Both sit in sentences this order froze.
2. CHANGELOG line for Tasks 56 and 56b, yes or no?
