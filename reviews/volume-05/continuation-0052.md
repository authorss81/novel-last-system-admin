# Continuation 0052 — Chapters 705–714

**Review pass, findings and repair. The batch was not restarted, the plot was not changed, no date was moved, no card was rewritten, and no title was touched. Every finding in `logs/continuation-0052.review.log` is recorded here, including the two that are not a writer's to fix and the one the reviewer got wrong.**

## Verdict

The review returned six findings. Four were concrete defects inside the ten chapters and all four are repaired in the prose. Two are structural and belong to a human. One item in finding 5 was checked against the real 2022 calendar and is correct as written; it is re-worded so the next reviewer does not have to re-raise it. Nothing about the family, the engine or the volume's direction was altered.

## 1. The two structural findings, and what the repair did about them

**1A. The manuscript has left the novel.** `NOVEL_SPEC.md` and `outline/series.md` describe *The Last System Admin*: a male lead, Jonas, repairing magical permissions in a city running on the Lattice. The last chapter anywhere in Volume 05 naming Jonas is **0263**; the last naming Sanaa is **0220**; the last use of *permission*, *lattice* or *CivicCore* in the volume is **0261**. None of the volume's own assigned pressure — a river disaster and mutual-aid permissions — and none of its planned climax is on the page.

**What the repair did: nothing, deliberately.** No plot changed, no character was given knowledge of it, the drift was not narrated, Jonas was not brought back for a beat. This is now the sixty-fourth prompt to flag it, and it is the first item in `state/open-threads.md`.

**1B. Volume 05 cannot be closed.** `ls chapters/volume-05/chapter-*.md | wc -l` gives **520**, which is 714 − 195 + 1, counted off the files, against an outline range of 195–242. `outline/volume-05.md` forbids a writer to write a volume-close prompt, and the 0053 prompt correctly refuses to write one. The consequence is that the runner keeps producing blocks with no path to a close. **This needs a human ruling now, not on prompt sixty-five.** No outline was rewritten to hide it and no chapter was moved.

## 2. Verbatim reuse across chapters — all four gone

| Reuse | Where | Repair |
|---|---|---|
| `The tap answers with a bead that grows and lets go.` | closing line of **both** 0705 and 0710 | kept in 0705, which is the chapter the device is born in; 0710's close rewritten |
| The full bowl-emptying paragraph (tips it into the bath, bead and small ping) | **both** 0705 and 0710 | 0710 rewritten: the water goes down the side of the tub in one sheet, the cloth is laid flat on the tiles instead of folded, and she counts the bead **once**, which she has never done before |
| `At dark she goes to the bathroom under the landing with her hands cold and empties the bowl.` | **both** 0705 and 0710 | 0710's stamp changed to carry no time adjective, because the time is now carried by the sequence |
| `They talk about water after, because water will not sit.` | section header in **both** 0713 and 0714 | kept in 0713; 0714's header rewritten around the empty jug and the tap |

**The check, with the method, so it can be re-run.** All ten files are stripped of headings, datelines and CAPS blocks, lowercased, reduced to letters and digits, and split into sentences of eight words or more. Every sentence is keyed; a key appearing in more than one file is a reuse. **Result: zero repeated sentences across the ten files.**

## 3. Internal chronology reversed in six of ten chapters — all seven fixed

The `---` rule fell at a paragraph end rather than at a turn, so the day ran backwards. The review's own examples: 0714 pegging washing "at the middle of the day" after the sister had arrived at the end of the day, and 0713 showing the sister the stool "before they eat" placed after they had eaten.

**The repair is block movement, not rewriting.** Whole `---`-delimited blocks were rearranged so the day runs forward, and the prose inside them is the prose that was delivered. The only textual edits were to sentences that named a time their new position no longer supported.

| Chapter | Was out of order | Moved |
|---|---|---|
| 0705 | yard at middle of day sat after the meter woman had gone and after the kettle | yard and the bathroom look moved ahead of the knock; the kitchen-visit block moved ahead of the kettle |
| 0706 | "middle of the day with the gates" sat after two end-of-day blocks | gates moved to the middle; eating moved before the run is sighted again |
| 0707 | "spends the end of the day" sat before two blocks that were earlier | the time stamp removed from that heading so the evening belongs to the two blocks that actually close the day |
| 0708 | "eats at the middle of the day" sat after the sister arrived, the tea and the door | the eating moved ahead of the sister's arrival |
| 0712 | "eats in the cab at the middle of the day" sat after four end-of-day blocks | the cab moved to the middle of the day |
| 0713 | showing the sister the stool, and mending the lid, sat after the soup was eaten and the bowls washed | both moved ahead of the eating |
| 0714 | pegging at middle of day, counting pegs, and blacking the stove sat after the sister's arrival | all three moved ahead of it; the sister arrives after the washing is in |

**The check.** A time stamp was extracted from the first line of every block, scaled 0 = first light through 6 = dark, and each chapter's sequence printed. **Every chapter now reads forward. Zero inversions across the ten.** 0709 and 0711 were measured against the same instrument, were already forward, and were left alone.

## 4. Near-duplicate staging inside 0710

The front-room doorway was staged twice ("again before dark" and "before dark") and the leaflet lass at the gate twice. Both pairs are collapsed to one scene each, and no material is lost: the brush stepped over on the way back from the doorway is folded into the remaining doorway beat, and the gate walk she makes **on her own** is kept whole, retimed and retitled so the lass is the only other person at that gate. **0710 is now one gate scene and one doorway scene, each with a different turn.**

## 5. A CAPS block that contradicted its own body

`chapter-0714.md:7` read *Her sister is on her own step at the end of the day.* The sister arrives off the front path, stands on **this** woman's step, and is inside at the kitchen table by the last block. It now reads that the sister comes off the front path at the end of the day and that the two of them are on the step together until dark.

**This is the exact defect class the 0053 prompt names for its own reviewer, and it shipped in the batch the prompt was written from.** It is recorded in the continuity block as well as fixed, because a defect that the handoff names and the batch repeats is a process defect, not only a prose one.

## 6. Story-craft vocabulary in the prose

The review's example, 0714:23, *"because water is the subject and will not sit"*, is the author talking about their own apparatus, which the 0052 prompt bans.

| Phrase | Copies | Where | Repair |
|---|---|---|---|
| `because water is the subject and will not sit` | **6** | 0708, 0710, 0711, 0712, 0713, 0714 | all six out; each replaced with something in the room or on the person, none naming a device |
| `the not-asking is the engine in her and not outside her` | **5** | 0705, 0707, 0709, 0710, 0712 | all five out; "the engine" is the prompt's own word for the family and printing it in prose is the same fault as printing "the subject" |

The van's **engine** is a real engine and was left alone in 0706, 0707, 0711 and 0712. The sweeps for both phrases now return zero across the ten files.

## 7. One rhetorical formula three times in 0714

The chain *"reading would mean asking, and I am not asking"* stood at three places. One is kept, at the drawer, where it is the hinge of the chapter. The other two are rewritten: one becomes a reason given out loud to her sister at the step, and one becomes a plain decision on the line while she pegs. A formula is a device, and a device repeated three times in one chapter is a defect.

## 7A. A canon conflict the review did not raise, and the pass found anyway

`chapter-0713.md` showed the sister the ash stool **at number ten**. The stool is not there. The binding rule in the 0053 prompt is *STOOL FRONT NINE NOT KITCHEN. SECOND STOOL FRONT TWELVE SEPARATE*, and the stool with nothing under it since 5 November belongs to number nine — which the chapter's own first block stages correctly, four blocks before contradicting itself, with the jug of soup already steaming on the table of the wrong house.

**Repaired without moving anybody:** the sister now comes to number nine in the middle of the morning, is shown the stool in number nine's front room, and follows her down the path with the bread to number ten, where the rest of the chapter happens. The dateline, the subject line, the card and the title are unchanged. No house changes hands and no object moves.

This is the fifth rule the 0052 prompt names — *open the file and ask whether it describes itself* — and no instrument caught it. It is the third time in this repository that a read-back done with the eyes has found what every count was silent on.

## 8. The item in finding 5 that is already correct

The review reported that `continuation-0053/PROMPT.md:50` sets the floor as Sunday 3 April 2022 while the table dates 0715 to Monday 4 April, and called it a disagreement by a day. **It is not a disagreement, and the arithmetic was re-run rather than argued with.**

- 0714 is Thursday 31 March 2022. **Verified on the real calendar.**
- A gap of three from 31 March is **Sunday 3 April 2022**. The floor is the earliest legal date, not the chosen one.
- The table's first rung, **Monday 4 April 2022**, is a gap of four, which is inside the permitted band of three to seven.
- The whole ladder re-verified: gaps 4/4/6/4/3/5/4/3/5/4, sum 42, span from 0714 to 0724 of forty-two days, no ninth, no eleventh, no two dates alike.

The ladder is right. **The sentence was ambiguous about the difference between a floor and a choice, and a floor that a reader takes for a booking is a floor that will be flagged again.** It now says so in words. No date was moved.

## 9. State-file and pipeline findings

- **`state/continuity.md` and `state/current.md` had no 0052 block.** The 0051 pass recorded a note in `batch-summaries.md` saying the substance lives in the other ledgers. `AGENTS.md` names continuity and is controller-owned, and a note in one ledger does not replace the file the controller names. **Both now carry a Continuation 0052 hand-over block.** Nothing was archived, truncated or deleted to make room.
- **No review artifact for 0049–0052.** `reviews/volume-05/` ended at 0048. This file closes the gap for 0052. The gap at 0049, 0050 and 0051 is a records failure and not one this pass can fill honestly, because the reviews for those blocks were never written.
- **`state/phase-ledger.json` is roughly fifty-two continuations stale.** It still reads `phase-002-batch-plan`, volume 1, batch 1, status `planned`. It is controller-owned and was not opened.
- **`dist/*.epub` is one batch behind.** Built by a workflow. Not built by hand.
- **Total state footprint is about 12 MB** and grows by roughly 2 MB per block. `state/live-canon.md` points writers at block pointers, which is a workaround for a file that has outgrown its role. **The pointer discipline is right and the size is a human's problem.**

## 10. Chapter length, published and not padded

The review noted the trend. It is real and it is the eleventh block running.

| | 0705 | 0706 | 0707 | 0708 | 0709 | 0710 | 0711 | 0712 | 0713 | 0714 |
|---|---|---|---|---|---|---|---|---|---|---|
| Before | 2,201 | 2,186 | 2,053 | 1,908 | 1,983 | 1,930 | 1,888 | 1,855 | 1,851 | 1,845 |
| After | 2,222 | 2,185 | 2,079 | 1,907 | 2,014 | 1,921 | 1,915 | 1,884 | 1,952 | 1,967 |

Total 20,046 words by `wc -w` over ten files. Eight chapters sit below 2,200.

**`PHASE_SYSTEM.md` line 311 asks for approximately 2,200–3,200 words and the same line says *never pad or split a complete scene solely to meet a number*.** The only two available moves are the two the guide forbids, so **nothing was padded.** The review is right that the chapters are thin; the repair publishes the measurement rather than buying the number with filler. A human may want the floor hardened, or the prose allowed to be thinner, and that is a human's call.

## 11. What checked out clean

Worth recording, because the writer-side measurement discipline is intact and the review confirmed it: the chapter-file count claim, the four-ladder and three-box object census, the fact that dialogue is present in all ten chapters, and the whole of the 705–714 weekday ladder.

## 12. What is now in the files

| File | Change |
|---|---|
| `chapters/volume-05/chapter-0705.md` | five blocks reordered, one time-stamp paragraph reworded, author-talk line replaced |
| `chapter-0706.md` | six blocks reordered, one referent fixed |
| `chapter-0707.md` | one heading de-stamped, author-talk paragraph replaced |
| `chapter-0708.md` | one block moved, one heading reworded, one repeated action corrected, author-talk replaced |
| `chapter-0709.md` | author-talk paragraph replaced |
| `chapter-0710.md` | two duplicate blocks collapsed, closing beat rewritten, two author-talk sentences replaced |
| `chapter-0711.md` | author-talk sentence replaced |
| `chapter-0712.md` | six blocks reordered, one heading reworded, two author-talk sentences replaced |
| `chapter-0713.md` | five blocks reordered, two possessives and one sentence break fixed, author-talk replaced, two headings reworded, **the stool returned from number ten to number nine** |
| `chapter-0714.md` | six blocks reordered, roster line corrected, washing continuity resolved, two of three repetitions of the asking formula rewritten, author-talk replaced, duplicate header rewritten |
| `state/continuity.md` | Continuation 0052 hand-over block appended |
| `state/current.md` | Continuation 0052 hand-over block appended |
| `workspace/volume-05/continuation-0053/PROMPT.md` | one calendar sentence reworded; no date moved |
| `reviews/volume-05/continuation-0052.md` | this file |

**No `.done`, `.blocked`, `.retry-after` or `.attempts` marker was created, touched or moved. No outline, bible, card, ledger or planned plot was altered. No dateline was moved and no title was changed.**