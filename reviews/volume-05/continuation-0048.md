# Continuation 0048 — Chapters 665–674

**Review pass, findings and repair. Chapters, dates, cards and plot unchanged. Every finding in the review log is recorded here, and the six numbered defects are fixed in the prose.**

## Verdict

The reviewer found one finding that outranks the rest and six concrete defects in the delivered chapters. All six are fixed. The first finding is not a writer's to fix and is now escalated, in `state/open-threads.md`, in `state/current.md` and as the third ruling in §6 of `workspace/volume-05/continuation-0049/PROMPT.md`.

## The finding that outranks the rest

**The manuscript has left the novel.** `NOVEL_SPEC.md` and `outline/series.md` describe *The Last System Admin*: a male lead, Jonas, repairing magical permissions in a city running on the Lattice. The last chapter anywhere in Volume 05 that names Jonas is **0263**. The last that names Sanaa is **0220**. "Lattice," "permission" and "CivicCore" appear **zero** times in a ten-chapter sample running from 264 to 674. From roughly chapter 264 onward, Volume 05 is a quiet domestic serial about six anonymous people in "this borough," with no protagonist, no System, no urban fantasy, and none of the volume's own assigned pressure, which is a river and mutual-aid permissions. Volume 05 holds **480 chapter files** against an outline range of 195–242.

The reviewer's recommendation was to escalate this to a human decision now: restore Jonas and the Lattice, or amend the spec to describe what the manuscript has become. Another ten chapters will not do it.

**What the repair did about it: nothing, deliberately.** No plot was changed, no character was given knowledge of it, the drift was not narrated, and Jonas was not brought back for a single beat. A writer may not do any of those things. It is now the first item in `state/open-threads.md`, the first line of the after-674 block in `state/current.md`, and the third ruling in §6 of the 0049 prompt, flagged fifty-eight prompts and counting.

## The six defects, and what was done

**1. Chapter length had collapsed about 65% against the immediately preceding batch.** `PHASE_SYSTEM.md` line 311 sets 2,200–3,200 words.

| Batch | Range | Mean |
|---|---|---|
| 655–664 | 2,550–3,543 | ~2,944 |
| 665–674 as delivered | 861–1,972 | ~1,178 |
| 665–674 after repair | 2,206–2,417 | ~2,249 |

All ten are now inside the guide. The review named the cause correctly and the cause was in a writer-authored file: the `---` rule in `bands-665-674.json` put sixteen to eighteen horizontal rules in each chapter, and that chops a scene into one- and two-sentence strips. The rule is amended to four to twelve, each at a real change of place, time or turn.

**2. Zero dialogue across all ten chapters.** `grep -c '"'` returned 0 for every file, against 3–12 dialogue lines in 655–662. `AGENTS.md` requires dialogue in every chapter and is controller-owned, so the ban in the writer's own band file lost to it. The ban is lifted, dialogue is required, and the word is now measured rather than banned. 0666's girl at the fence, which the review singled out as "the one live moment in the chapter" rendered as summary, is now a scene.

The repair is only a repair if the family survives it, and it does. Ten strangers now speak in this borough and not one of them asks the question: a gas man steps over the brush and asks whether she is all right upstairs; a surveyor on an answerphone asks to be let into a room in her own house; a lad with a parcel does not ask who it is from; a council man with a form asks whether there is water staining and is told there is not. The engine of 0044 and 0045 is still the engine and it is harder to see now, because there is somebody in every chapter who could have asked.

**3. Meta-language leaked into the prose.** `chapter-0674.md:83` read *"the first time in this account that she got past a thing by stepping over it has become every time."* The band file's own `this_chapter` prohibition shows the rule was known and the variant was missed. The line is gone, replaced with an in-world sentence, and the band file's prohibition now names `in this account`, `in these ten chapters` and any other variant that steps outside the story. All are at zero across the ten.

**4. Self-reported metrics were wrong.** Two of the three headline figures in the batch summary and in `continuity.md` were false.

| Metric | Published | Actual as delivered | After repair |
|---|---|---|---|
| Total words | 11,779 | 11,779 ✓ | 22,492 |
| `still` total | 41 | **43** | 52 |
| `still` per chapter | 6/5/6/4/1/5/3/6/3/2 | **7/3/6/4/1/6/4/6/2/4** | 4/5/9/5/2/5/4/10/4/4 |
| `said` | 8 | **9** | 34 |
| `---` row | 18,18,18,18,16,18,16,16,16,18 | ✓ | 8,9,6,8,6,11,7,7,7,8 |
| Quoted-speech lines | not published | 0 in every file | 3–46, no nils |

The review also caught the real error behind defect 1: the `---` row was described as "reported not fixed," and 16–18 rules per chapter is not a neutral observation, it is the cause. The `reported and not touched` stance is withdrawn in the 0048 band file and in the 0049 prompt.

**5. Card drift in 0672.** The card ends *"and nobody sees him."* The delivered chapter ended on the bare words `He drives on.` with the turn asserted only in the subject line. It is now staged: a figure at a kitchen window with her back to the glass, a bus going past, and his hand on a door handle that he takes off again. He also decides in the scene that he does not know what her face looks like.

**6. No review was recorded.** `reviews/volume-05/` had files through `continuation-0043.md`; 0044 to 0048 were missing. This file is the record for 0048. **The recommendation to run the missing reviews for 0044 to 0047 is left open, because a review is a reviewer's file and a writer does not write one for a phase it did not read.** It is listed in the open threads.

## What the repair found that the review did not

- **0667 contained a sentence that was not English**: *"He knows the gate is done because he stood at his own kitchen window is not true."* It now reads that he went past the end of the road once, in the last week of August, without slowing, which also gives 0672 a ladder, since 0672 is the first time he stops.
- **0666's dateline promised two houses** and the delivered chapter wrote one. The second is now on the page, with a bed frame, a headboard, a daughter with the paperwork, and a question about the plaster that is not asked.
- **0668 explained in narration why a figure had been left unaged.** The sister is now simply not aged, which is what the rule asked for.
- **Banned words also occurred in plural and third-person forms.** `holds` appeared three times, once as the answerphone's delete instruction in 0670. The band file's boundary list is extended to those forms.

## What held up

The single-object discipline worked where it was tested. The three brushes — passage floor, man's plastic bag, stranger's side pocket — stayed separate, and 0666 still disowns the passage-floor brush explicitly. The stool, the green chair and the rush-seated chair each hold one room. Water tracks plausibly from a bathroom ceiling to a front room ceiling across the ten chapters, and the family's proof, that the thing arrives where it was not meant to go, is stronger now that a man in a van is the one who makes the water's progress visible without knowing it. The band file's self-correction of 0661's drawer was handled in prose rather than hidden.

Banned-word compliance was and remains clean. The calendar is clean: all ten weekdays verify against the real 2021 calendar, gaps 3 to 7, no ninth or eleventh, no duplicates. That discipline is real and it was kept.
