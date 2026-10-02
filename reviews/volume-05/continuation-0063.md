# Continuation 0063, chapters 815 through 824 — review

Review date: 2 October 2026. Ten chapters read whole. `workspace/volume-05/continuation-0063/bands-815-824.json` read. The six state blocks this phase wrote read. Both prompts written in the same commit read whole — `continuation-0063/PROMPT.md`, which instructed this block, and `continuation-0064/PROMPT.md`, which is the live instruction for the next one — because the writing of both happened in one run and both are what this phase handed on.

**An external reader reviewed this phase first and returned seventeen findings. This review is the record of what was done with them, of what this reader checked again independently, and of what is left standing for a human.** The external reader's four highest-priority items were the calendar bounds in the live prompt, a wrong canon fact that had propagated into two state blocks, and the stale dispatch pointer. Two of those four turned out to be mis-attributed or unverifiable and are recorded below as such rather than repeated as fact.

## What the block is, in one paragraph

Five houses and five standing figures in a rotation of five, one job to a chapter, each job found by the person who lives in the house and each job finished by that person inside its own day. **The family declared before any prose existed — work nobody asked for, done to a measure nobody set, where the whole of every chapter is the point at which the person stops — holds, and the ten chapters do not run the fault that has killed the two blocks before it, because there is no second pair of hands in any of them and so there is nobody to count.** No arithmetic engine, no telephone, no water drawn anywhere in the ten, no new figure at all, and the man off the ring road sitting out for the seventh block running.

## Verified off the files, not off the summaries

| Claim | Result |
|---|---|
| Words 2522, 2074, 2024, 2211, 1959, 2083, 1953, 2006, 1761, 2084, total 20677 | exact, by `wc -w` on each file whole |
| Scene breaks 2 in each, 20 in all | exact |
| Banned thirty-nine plus six watched, whole file including the all-caps paragraph | zero in every chapter |
| `said` at 1 across the ten, in 0820, against a cap of five | exact |
| Declared ordinary word `line` at 1,4,15,16,0,1,9,0,5,7 = 58 | exact, unmoved by this repair |
| Numerals | the chapter number and the year only |
| One all-caps paragraph in each, all at line 5 | 10 of 10 |
| `ls chapters/volume-05/chapter-*.md \| wc -l` | 630 |
| Shared ten-token body spans, dateline inside the body | 0 across all 45 pairs, 0 inside any chapter |

**The chapter-date chain stands.** Ten gaps — 3, 5, 3, 3, 4, 3, 6, 3, 3, 5, counting the incoming one from 0814 — and thirty-eight days from Tuesday 23 May to Friday 30 June 2023, re-derived off the real calendar by this reader rather than copied. Seven distinct weekdays, Friday twice, Saturday twice, Tuesday twice, nothing on the ninth or the eleventh, no two sharing a date. The chain is right; **the two bound sentences printed around it were not, and that is finding 1 below.**

## Findings fixed in this repair

**1. Four wrong weekday names in the two calendar bounds of 0063's own prompt.** It printed *Wednesday 22 June to Wednesday 1 August* and *Wednesday 22 June to Wednesday 28 July*. The real bounds are **Thursday 22 June to Tuesday 1 August** and **Thursday 22 June to Friday 28 July**. Both are now correct in `continuation-0063/PROMPT.md`. **The paragraph that carried the error ends by instructing the writer to take the dates off the real calendar, which is what would have caught it, and no measure in the block's own band file ever looked at a weekday name.**

**2. The same defect in the live prompt for 0835 onward, and worse.** `continuation-0064/PROMPT.md` printed *Monday 29 July to Friday 7 September* and *Monday 29 July to Monday 5 September*. The real bounds are **Sunday 30 July to Friday 8 September** and **Sunday 30 July to Monday 4 September** — two wrong weekdays and two wrong dates in each bound, in the file the next writer will obey. **The chapter-date chain itself was correct and is untouched.**

**3. The live prompt contradicted the finished files twice.** It said *0063 came to 20 and thirty-six more were cut in its own drafting pass* — impossible, since the ten files hold exactly 20; it came to **56** and thirty-six rules were cut to finish it there. And it said the man off the ring road had sat out *seven blocks, 0057 through 0064*, which is eight. Both corrected. The off-road sentence in 0063's own prompt reads 0057 through 0063 and is right, so this was a fresh off-by-one in the newer file.

**4. A closing image that is not in its chapter, propagated into canon.** 0818 was declared to end on *the clippings going over the front of the path on the wind*. No word *clipping* occurs in that chapter; what the wind takes there is **arisings**, off a cut edge, and it puts a green film along the top of the kerb. The wrong noun had already been copied into `state/continuity.md` twice and `state/batch-summaries.md` once as settled canon. **The prose is not at fault and was not touched: the arisings, the wind and the film are all on the page. The canon now reads arisings** in the band file, in the 0063 prompt, in the two state blocks and in the batch summary, and the three-word description reads *the arisings going*.

**5. Three wrong pronouns in the plan, all in the same direction.** The 0063 prompt's ending list said *saw* for 0815, where the chapter cuts the root square with a spade and says why; *she* for 0819, which is a man at the unit; and *her* for 0821, which is also a man. The band file had the 0819 pronoun right and the 0821 one wrong. All corrected in both files. `state/current.md` had already recorded the first three as corrected — they had been corrected on paper and not in the committed files, which is the fault this finding is really about.

**6. Chapter 0815 broke the block's own second-person rule and displaced its own engine.** The prompt and the band file both put the sister at twelve *in the kitchen with the door open and not coming out*, and the prose brought her to the kitchen step, gave her an opinion on the work, told the protagonist what to do about it, and handed her four lines of craft reasoning about lilacs. Card 0815's engine is the difference between a base that has moved and a base that has not. **The sister now stays in the kitchen and the hour of talking is about the front step and the flue, and neither of them says one word about the flags or the lilac or the root**, and the card's engine stands where it stood. Nothing else in the chapter was moved: the trade is intact, the cut root is intact, the last three paragraphs are intact.

**7. A clause stated twice, word for word, in 0821's last two paragraphs.** *a wire on it is rusted through* appeared in both. The second is now **the gravel board at the near end carrying the board above it with nothing under it but air**, which is a fact about the fence and not a repeat, and it is the better of the two endings. Note that the wire is still rusted through in 0821's own body at line 79 — it was the *echo*, not the fact.

**8. 0815 stated its stop twice in consecutive sentences.** *and then she stops cutting it* followed immediately by *She stops cutting it because she can see where it goes.* The first clause is cut; the second paragraph carries the beat alone. That also removed one instance of the watched phrase *and then*.

**9. Two next-batch directories in one commit.** The established pattern is one new directory per writer run, and this run added both `continuation-0063/` and `continuation-0064/`, so 0063's prompt was committed holding a page count of 620 while its own ten chapters sat in the same commit. **0063's prompt now opens with a banner saying the block is written and closed, that the page is at 824 and 630 files, that the file is a record and not an instruction, and that a writer who picks it up as live will write a second 0063 on top of a finished one.** It was not deleted, because its band file and its first wordings are the audit trail for the four plan errors the block admits to.

**10. Two more self-contradictions in the 0064 plan, found while checking the above.** Its band file says the second person must *not hold anything and not touch it*, and then allocated 0825's sister to *put the stones down where she is told to*. **She now stands at the gate while the stones go down through it and picks none of them up**, in both the prompt and the band file. And card 0834 rested on the protagonist having *told her sister* that you take the top off a lilac and you have three — a line that lived in the 0815 sister scene this repair removed. **The card now rests on what she found out at the bar in May**, which is on the page.

## Two of the external findings do not survive checking

**The claim that 0064's prompt records *0818 the clippings* as settled canon is not supported.** There is no occurrence of *clipping* anywhere in `continuation-0064/`. The phrase is in 0063's prompt and in two state blocks, and those are what was fixed. **Nothing was changed in 0064 for a fault it does not have, and a reviewer who repeats that claim will send the next writer looking for a word that was never there.**

**`measure_runs.py` is not duplicated *byte for byte* into every directory** in the sense implied, but the duplication is real and this reader has to record it: 0063 and 0064 each add an identical 136-line script, 272 lines for one script, and the right home is `scripts/`, which is controller-owned and was not touched. **This is a fleet-level fix and not a repair-pass fix, and it is the fifth review to raise it.**

## Structure the measures cannot see, and what was done about it

The external reader's sharpest observation is that the apparatus has inverted the priority: a 103-line prompt and a 302-line band file of counting rules now stand in for a human read, and the 0064 prompt's own sentence *a ten-token span finds a copy, it cannot find an error of fact* concedes it. **Findings 4, 5, 6, 7 and 8 above are the proof: all five passed every measure in this block's own band file at a shared-span count of zero.** Two things were done inside the files this phase is allowed to touch, and neither changes a card, a band, a date or a family.

**Four checks are now named in the 0064 prompt, each one off a real failure in 815 to 824: the closing image must be greppable in the finished chapter and written in the words the chapter will use; every pronoun is read against the roster after the prose and not before; the last three paragraphs of each chapter are read side by side and no fact may stand up twice; and the visitors paragraph is a floor and not a ceiling, with the 0815 scene named as what happens when it is ignored.**

**And the reading order was made survivable.** `state/current.md` is 938 KB and `state/continuity.md` is 5.7 MB, both append-only across sixty-three blocks, and the handing-on instruction says to read the whole of them. **The 0064 prompt's read list is unchanged, because it already points at named blocks at the end of each file, and those pointers are the only part of the state a writer can afford.** What the state files themselves still need is a human decision about compaction, and it is recorded in `state/current.md` as a human's and not as a writer's to settle.

## Left to a human, and not touched by this repair

`state/phase-ledger.json` still reads phase-002-batch-plan, volume 1, chapters 1–10 against a manuscript at 824. **It is controller-owned, was correctly left alone, and this is now the fifth review to say so — which is the point: a flag nobody may act on stops being a flag and becomes a habit.** The volume holds 630 files against an on-page range of 195 to 242 and no figure anywhere for its end; the protagonist has been off the page since 0263, now seven blocks and sixty chapters; the System has not appeared in this block at all; the freeholder has not come; the line at ten is not put right; the ladder stays folded. **Volume 05 at 630 chapters against a guidance of 40 to 80, with a further eight continuations planned and no close in sight, is the largest single thing in this review and it is not a writer's to settle.** Reviews for 0060, 0061 and 0062 are still absent from `reviews/volume-05/`, which leaves the audit trail for three blocks unverifiable; this review does not manufacture them.

## Addendum, the repair phase of 2 October 2026

**Two chapter files were opened and both edits were surgical.** 0815 lost the sister scene it was not allocated and one repeated clause; 0821 lost one repeated clause and gained one sentence. **No plot moved: no card changed its job, no band changed, no date moved, no family changed, no standing object changed, no standing prohibition was touched, and the planned volume direction is exactly as it was.** The prompt repairs corrected facts and removed one contradiction; the 0834 card keeps its stop, its subject and its ending.

**Figures re-taken after the repair, because the repair moved prose and this reader checked rather than assumed:** 630 chapter files. Words 2522, 2074, 2024, 2211, 1959, 2083, 1953, 2006, 1761, 2084, total 20677, median 2049, by `wc -w` on each file whole. Scene breaks 2 in each, 20 in all. Banned and watched words zero, `said` at 1, one all-caps paragraph in each, the only numerals the chapter number and the year, declared ordinary word *line* still at 58. **Shared ten-token spans 0 across all 45 pairs and 0 inside any chapter — and the repair itself was measured, not asserted: 0815's new sister scene was rejected once for sharing *the whole of what passes between the two of them* with 0819 and was rewritten before it stood.**

**Card 0824 is not a close and is not called one, and no card in 815 to 824 is a close and none is called one.**
