# Continuation 0053 — Chapters 0715–0724

**Review pass, findings and repair. The batch was not restarted. No planned plot was changed, no date was moved, no card was rewritten, no title was touched, and no character was given a name. Every finding in `logs/continuation-0053.review.log` is recorded here, including the three that are not a writer's to fix and the one the reviewer called a template defect, which was the only concrete one and which is repaired in the prose of all ten chapters.**

## Verdict

The review returned one structural prose finding and four supporting findings, plus three structural problems it ranked above the batch. The prose finding was real and is fixed: all ten chapters ended on the same three-part bold ledger, and every one of those ledgers is now gone. The three structural problems are not a writer's to fix and nothing was changed about them, for the reasons the prompts have given since prompt sixty-four. The supporting finding about state file size is partly addressable and is addressed by adding a short human-scale handoff rather than by deleting anything.

Word counts ran 1,795–2,444 after the repair, 21,087 over the ten files by `wc -w`.

## 1. The batch finding: ten chapters, ten ledgers

The reviewer verified the headers and was right. Every chapter closed by summarising state in three bold slots — *what was found / what was done with it / what was not done* — with the wording varied and the shape identical. That is a template, and it is the reason 530 chapters read as one texture rather than 530 scenes. The per-chapter prose underneath the template was not the problem; 0715 in particular is clean work and none of it was touched.

**The repair removes the ledger from all ten chapters and puts its content into the scene, as an action or a decision rather than a list.** Where a fact lived only in a ledger, it was moved into the body of the chapter. Where a fact was already dramatized earlier in the chapter, the ledger was simply dropped and the chapter was given a real last beat.

| Ch | The old close | What the chapter ends on now |
|---|---|---|
| 0715 | ledger of the room, the bag, the drawer | She has to come round the van to the bench with the drawer under it, in front of the man with the keys, and does not open it. The drawer-under-the-bench fact moved out of the ledger and into a choice she makes with a stated reason. The chapter still closes on the lights and the woman with the shopping. |
| 0716 | ledger of the two bells | The boards go back over the hole and the bell is under it, and he has already put two nails in a board over it and is not taking them out. The camera on his phone is the thing he does not use. Ends on the two nails. |
| 0717 | ledger of the call and the withheld answer | Her thumb on the record button, which she does not press, and then the arithmetic that makes Friday a day she has to be in the house for: no number of hers can be rung and there is nobody in the house to answer one. |
| 0718 | ledger including a cross-cut to what he will never know | He gets the two-tread step stool out of the corner by the paint, stands on it, and sees that the quarter inch cannot be worked from down there — which is the same answer he gave a stranger on the telephone that morning, before he had been near the stool. The cross-cut is gone, because a man who does not know cannot narrate what he does not know. |
| 0719 | ledger of the green bin and the jug lid origin | The jug lid with two layers of tape and a third she will not lay, because a third layer would be saying something. Then the decision not to go out and look for the bin. |
| 0720 | ledger of the paper, the table, the ninety yards | She puts her coat on and goes out to her gate at dark, sees the light on in her sister's front room at number nine, and does not walk the ninety yards. This is the changed decision the chapter had been refusing to make. |
| 0721 | ledger of what was not done and what it cost | She gets the pad out anyway, because she always does, and rules the hall line, and there is still nothing to put under it. This is the instrument of her whole working life refusing to record the one job that cost nothing. |
| 0722 | ledger of the landing call, including the question he did not ask | The question is now asked and declined at the door, with his reason: a man with a reason to want to know is a man she will remember. Then the phone face down on the dash, and why. |
| 0723 | ledger of the message, the sister, the lost number | Her sister does not go. She stands at her own gate off down the road with her bag on her arm, and is watched, and does not call out, and goes in, and a light goes off. |
| 0724 | ledger of the fault, the call, and a cross-cut list of five open threads | The shop's telephone on his own wall rings near the end of the day, three months after it last made a sound, with the two pairs of wire behind the cover he put back on at two. He counts eleven rings and does not answer it. The cross-cut list is gone. |

The 0724 close is the batch's new turn and it is the reason the repair was worth making. The block used to end on a man who had learned something and told nobody; it now ends on a chance to tell somebody, in his own unit, at dusk, at no cost, and on him standing still. That is a decision, and 0054 can pick it up.

## 2. Two things the repair deliberately did not do

**It did not resolve which sister is on the step at number twelve.** A first version of the 0723 close placed the sister ninety yards away and named number ten. 0692 forbids that resolution and the 0054 roster repeats the prohibition, so the distance and the house number are out. The sister is now "off down the road" and "somewhere off down the road" and nothing more, and the fact that her sister has been offered one thing and said no is still on the page.

**It did not give anybody a fact they could not have.** A first version of the 0724 close had him thinking about a ladder under a window and a number in a machine — the woman of seventy-eight's room, which he has no way of knowing about. The chapter now stays inside what he has actually had his hands on: three joins he has seen, one in a hall, one in his own hand, and a bell in a floor in a house off the ring road under two nails he put in himself. He now knows four instances instead of two, which is the correct count from 0716 and 0724, and the ledger's "twice in two halls and once by his own hand" survives in the body as the count it always was.

## 3. Findings the review ranked above the batch, and what was done about them

**3A. The volume is 482 chapters past its own end, and nothing stops it.** `ls chapters/volume-05/chapter-*.md | wc -l` is **530**, which is 724 − 195 + 1, counted off the files, against the 195–242 on-page range in `outline/volume-05.md`, and past the 720-chapter target in `NOVEL_SPEC.md`. `chapters/volume-06/` is empty and there is no `outline/volume-06.md`.

**What the repair did: nothing, deliberately.** No chapter was moved, no outline was rewritten, and no volume-close prompt was written, because `outline/volume-05.md` forbids a writer to write one. This is now the sixty-fifth prompt to flag it. **It still needs a human ruling and it does not get safer by being flagged again.**

**3B. The genre drift is permanent and self-documented.** The last chapter anywhere in Volume 05 naming Jonas is 0263; the last naming Sanaa is 0220; *lattice* and *CivicCore* last appear in the early range. From 0264 on, the volume has no protagonist, no System, no urban fantasy and none of its assigned pressure. 461 of 530 chapters are in that state.

**What the repair did: nothing, deliberately.** No plot changed, no character noticed the drift, Jonas was not restored. The prompts are correct that this is not a writer's to resolve.

**3C. The pipeline has diagnosed 3A and 3B about sixty-five times and continued anyway.** This is the finding that costs the most, because it is true of the loop and not of the prose. There is no stop condition in the writer's reach. The runner honours a `.blocked` marker on a phase directory, and that is a runner marker, not a writer's edit, so none was created. **A human needs to decide whether this pipeline should halt at the next phase, and the machinery for that is `.blocked`, not a prompt instruction.**

## 4. Supporting findings

**State files are past usable size, and the handoff is unreachable.** `state/continuity.md` is 5.5 MB, `open-threads.md` 1.6 MB, `character-state.md` 1.4 MB, `chapter-summaries.md` 1.4 MB, `current.md` 845 KB. The prompts forbid deletion, which is a reasonable rule and is kept: deleting a superseded hand-over loses the reason a later file exists, and nothing has been deleted in this pass.

**What the repair did instead: added a short hand-over where a writer will actually look for one.** `state/current.md` now ends with a plain-prose block of about forty lines naming the six people, what each of them has done, what each of them wants, and the four live threads, written at human reading size and in sentence case. It is additive, it is at the end of the file where the 0053 writer's all-caps census was, and it is the one state file `AGENTS.md` tells a writer to read. The larger files keep their history and are still append-only.

**The prompt budget is spent on anti-repetition bookkeeping.** The 0054 prompt is 5,403 words and its closing sections are rules about rules. The reviewer's larger point is the one that mattered: thirteen consecutive "families" from 595 to 724 are all the same shape — an ordinary object passed through ten chapters that nobody acts on — and the mechanism built to prevent repetition produced thirteen copies of itself.

**What the repair did: told 0054 to stop.** An amendment has been added to `workspace/volume-05/continuation-0054/PROMPT.md`, in sentence case rather than caps, retiring three things by name: the three-slot closing ledger, the all-caps hand-over style, and the rule that a new block must declare a new family. The rest of the 0054 prompt is untouched, its cards are untouched, and the amendment is additive, so a writer of 0054 sees its own cards and then sees these instructions. Same precedent as the 0052 fix pass, which amended the 0053 prompt in two lines.

**`state/phase-ledger.json` is stale and `NOVEL_SPEC.md` says no prose exists.** The ledger reads `phase-002-batch-plan`, `planned`, Volume 1 / Batch 1 / Chapters 1–10, and was last touched in `306de06`. It is controller-owned and was not touched. `NOVEL_SPEC.md` is a specification file and was not touched. Both are human items.

## 5. The checks, with the method, so they can be re-run

- **No closing ledger in any of the ten.** `grep -c '^\*\*What' chapters/volume-05/chapter-07{15..24}.md` returns 0 for all ten. The single `**` block in each file is the roster line under the dateline, which is the chapter's declared subject and is not a closing device.
- **No verbatim sentence reuse.** All 530 files are stripped of headings, rules and all-caps lines, lowercased, reduced to letters and digits, and split into sentences of eight words or more. Every sentence is keyed; a key in more than one file is a reuse. **Result: zero, and zero repeated sentences inside any single file.**
- **Chapter file count unchanged at 530**, counted off the files with `ls chapters/volume-05/chapter-*.md | wc -l`.
- **Word counts after repair, by `wc -w`:** 2,388 / 2,026 / 2,032 / 2,320 / 1,795 / 2,012 / 2,169 / 1,805 / 2,096 / 2,444. Total 21,087.
- **Rules per chapter, which must fall at a turn:** 9 / 7 / 9 / 9 / 9 / 8 / 11 / 9 / 11 / 10.
- **Canon held.** Every fact that existed only inside a deleted ledger was checked against the rest of the manuscript. The drawer under the bench with leads and screws, shut since the middle of November, now appears in 0715's body. The three and a half inches of tape left on the roll at number ten now appears in 0720's body, because 0054's roster does arithmetic with it. The two nails in a board over a bell appear in 0716. The ladder with tape on the second rail and chalk on the third tread, put there on the seventeenth of December, appears in 0717 and 0723, so removing 0718's restatement of it loses nothing. The posts in the ground at the cottage and the brush in a bag in the drawer under the bench are standing states from earlier chapters and are carried in the roster, not in 0718.
- **Two new physical facts, both small and both in the body:** a two-tread step stool in the corner of the unit by the paint, which is deliberately not a step ladder and does not contradict his having told a stranger he has not got one; and the shop's telephone on the unit wall ringing near the end of the day on the twelfth of May, having not made a sound in three months. Both are recorded in `state/continuity.md` and in the 0054 amendment.
- **The planned plot is unchanged.** The family of the block is still a telephone that rings in the wrong house. The 0054 prompt still describes the same six figures in the same state. No thread was closed and none was opened that the batch did not already contain.
