# Report-back, interim: Task 56e stopped before Part A (2026-11-08)

Order: `D:\Projects\hq\uni\ai-for-good-hackathon\task-56e-present-15s-order-2026-11-08.md` (Fable's corrected version). Branch `task-56`. No code changed. No commit. Nothing run beyond the reads below.

## Why it stopped

Item 3 says: check "The laws found do not settle this, so the gate did not allow it." against `onyx/gate.py` and the coordinator; if it is not true, stop.

The second half is true: a step with this verdict does not go ahead.

The first half is not true for every "Not enough evidence" label on the runs page. The gate gives this verdict in `_base_checks` (`onyx/gate.py` lines 821 to 837) for evidence faults, not for a reading of the law:

- "no clause cited" (the agent cited no law at all)
- "<clause> was not retrieved by <agent> for this step"
- "<clause> is not in the knowledge base"
- "<clause> has status ...; only VERIFIED text can carry a decision"
- "the quote is not N+ characters verbatim in a cited clause"

The gate never judges whether the laws found settle the question. That judgment is the adviser's abstention (coordinator, `abstain` event), which the page shows in its own box, not as an answer label.

On the ten runs the page shows (five scenarios, English and Arabic), the gate labels "Not enough evidence" carry:

- 6 times: "no clause cited"
- 1 time: "cabinet-66-2023:34(5) was not retrieved by care for this step"

(The 10 adviser abstentions are a separate box and keep their own words.)

## Question for hq (Fable)

1. What should the "Not enough evidence" label's first sentence say? A sentence true for every case above would be, for example: "The proposal did not carry the evidence the gate needs (a checked law, quoted word for word), so the gate did not allow it. The gate's reason is below." That is a suggestion only; hq writes the words.

## Facts found for the rest of Part A (not built yet)

- Item 2: the classifier's channels are the keys of `CHANNELS` in `onyx/agents/adviser.py`. Not yet listed in plain words; to be read when the build resumes.
- Item 4: the five team-written steps match `pending_proposal` in the scenario files (S1 6, S2 5, S3 3, S4 5, S5 4), as Task 56c found.
- Pins that will move in Part A: `tests/test_task_56c.py` ("SECS = 12"), `tests/test_report.py` line 528 (the side note quotes the fold name "Without the gates").

## Second stop (after Fable's addendum, same day)

The new "Not enough evidence" sentence is true for all 7 of those labels. But a count of every answer label on the ten runs shown shows a second problem, with the other three sentences:

| Label | With laws | With no laws listed |
| --- | --- | --- |
| Allowed | 20 | 23 |
| Held | 17 | 2 |
| Blocked | 7 | 3 |

On the 28 labels with no laws listed, "The laws it rests on are below" and "The gate's reason and the laws it used are below" would claim laws that are not there. The gate's own reason on those 28, as logged:

- Allowed, 23 (classify_channel 4, draft_reply 7, flag_gap 8, receive_objection 4): "every base check passed; this verb has no further condition". The verdict lists no clause.
- Held, 2 (route, S2 step 5): "the adviser answered INSUFFICIENT_EVIDENCE on S2-5: no VERIFIED clause permits route; held for a human".
- Blocked, 3 (propose_change 1, request_report 2): "deadline '...' is not a rules.json rule, value and unit".

## Question 2 for hq (Fable)

2. What do these three labels say when the verdict lists no law? One option: drop the last sentence's "and the laws it used" / "The laws it rests on are below" and show only the gate's reason, with no "Show the N laws" toggle. hq writes the words.
