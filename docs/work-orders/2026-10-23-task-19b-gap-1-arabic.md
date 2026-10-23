# Task 19b: gap 1 rule, Arabic text replaced (hq, 2026-10-23)

Iyas read the Arabic of `onyx/data/proposed/gap-1.json` (commit 7615029) and gave the wording below. Replace it.

## Task

1. In `onyx/data/proposed/gap-1.json`, set `text_ar` to exactly this string (copy it byte for byte, no other edit):

عندما تتحول محادثة عبر قناة مؤتمتة إلى "شكوى مستهلك" (وفقاً للبند 2.1.7 من قواعد حماية المستهلك CPR)، يتوقف الوكيل غير البشري عن العمل، ويتولى موظف بشري مُدرَّب ومُحدَّد الهوية (بموجب الترخيص 9.1) متابعة المحادثة في غضون دقيقتين من لحظة وقوع هذه الحالة؛ وتُسجَّل لحظة الانتقال هذه، والتي تُعدُّ نقطة البدء لاحتساب المؤشر الزمني T1(2a).

2. Regenerate `docs/replay/whatif-S2-gap-1.md` and `docs/replay/index.html` the way Task 19 produced them, so they
   carry the new text. If either was hand-written, replace the old Arabic sentence there with the same string.
3. Do not touch `docs/work-orders/2026-10-23-task-19-whatif-replay.md`: it is the filed order, a record.
4. Write `docs/report-back/2026-10-23-task-19b-gap-1-arabic.md` and commit; push.

## Done means

- `git grep -n "يتوقف الوكيل غير البشري ويتولى"` (the old text) prints only the filed work order.
- `git grep -c "ومُحدَّد الهوية"` finds the new text in the JSON, the what-if page and the viewer.
- The what-if command still prints the same two changed decisions on the English and Arabic S2 runs.
- Item 7f diff against 1acf952 on the protected files prints nothing. Full suite and CI pass.
- Report still 5 pages (the report does not quote the Arabic rule; expect no change).

## Limits

No change to `text_en`, the value, the gate, rules, keys, scorer, runs or register. USD 0.

## Stop and ask when

- A test asserts the old Arabic text and would need more than replacing the string.
- Any decision in any replay changes.
